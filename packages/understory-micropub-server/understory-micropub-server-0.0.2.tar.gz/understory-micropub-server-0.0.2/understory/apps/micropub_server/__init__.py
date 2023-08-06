"""A Micropub client for the Understory framework."""

import sh
from micropub import server
from understory import web
from understory.web import tx

app = web.application(
    __name__,
    prefix="pub",
    args={
        "channel": r".+",
        "entry": r".+",
        "nickname": r"[A-Za-z0-9-]+",
        "filename": rf"{web.nb60_re}{{4}}.\w{{1,10}}",
    },
    model=server.model.schemas,
)


def wrap(handler, app):
    """Ensure server links are in head of root document."""
    tx.pub = server.model(tx.db)
    yield
    if tx.request.uri.path == "":
        web.add_rel_links(micropub="/pub")


def route_unrouted(handler, app):
    """Handle channels."""
    for channel in tx.pub.get_channels():
        if channel["resource"]["url"][0] == f"/{tx.request.uri.path}":
            posts = tx.pub.get_posts_by_channel(channel["resource"]["uid"][0])
            web.header("Content-Type", "text/html")
            raise web.OK(app.view.channel(channel, posts))
    yield


@app.control(r"")
class MicropubEndpoint:
    """"""

    def get(self):
        """"""
        try:
            form = web.form("q")
        except web.BadRequest:
            channels = tx.pub.get_channels()
            entries = tx.pub.get_entries()
            cards = tx.pub.get_cards()
            events = []  # tx.pub.get_events()
            reviews = []  # tx.pub.get_reviews()
            rooms = tx.pub.get_rooms()
            media = tx.pub.get_media()
            return app.view.activity(
                channels, entries, cards, events, reviews, rooms, media
            )

        def generate_channels():
            return [
                {"name": r["name"][0], "uid": r["uid"][0]}
                for r in tx.pub.get_channels()
            ]

        # TODO XXX elif form.q == "channel":
        # TODO XXX     response = {"channels": generate_channels()}
        if form.q == "config":
            response = server.get_config()
        elif form.q == "source":
            response = {}
            if "search" in form:
                response = {
                    "items": [
                        {"url": [r["resource"]["url"]]}
                        for r in tx.pub.search(form.search)
                    ]
                }
            elif "url" in form:
                response = dict(tx.pub.read(form.url))
            else:
                pass  # TODO list all posts
        elif form.q == "category":
            response = {"categories": tx.pub.get_categories()}
        else:
            raise web.BadRequest(
                """unsupported query.
                                    check `q=config` for support."""
            )
        web.header("Content-Type", "application/json")
        return response

    def post(self):
        """"""
        # TODO check for bearer token or session cookie
        try:
            form = web.form("h")
        except web.BadRequest:
            try:
                resource = web.form()
            except AttributeError:  # FIXME fix web.form() raise Exc
                resource = tx.request.body._data
        else:
            h = form.pop("h")
            properties = {
                k.rstrip("[]"): (v if isinstance(v, list) else [v])
                for k, v in form.items()
            }
            resource = {"type": [f"h-{h}"], "properties": properties}
        try:
            action = resource.pop("action")
        except KeyError:
            permalink = tx.pub.create(
                resource["type"][0].partition("-")[2], **resource["properties"]
            )
            # web.header("Link", '</blat>; rel="shortlink"', add=True)
            # web.header("Link", '<https://twitter.com/angelogladding/status/'
            #                    '30493490238590234>; rel="syndication"', add=True)
            raise web.Created("post created", permalink)
        if action == "update":
            url = resource.pop("url")
            tx.pub.update(url, **resource)
            return
        elif action == "delete":
            url = resource.pop("url")
            tx.pub.delete(url)
            return "deleted"
        elif action == "undelete":
            pass


@app.control(r"channels")
class Channels:
    """All channels."""

    def get(self):
        """"""
        return app.view.channels(tx.pub.get_channels())


@app.control(r"channels/{channel}")
class Channel:
    """A single channel."""

    def get(self):
        """"""
        return app.view.channel(self.channel)


@app.control(r"entries")
class Entries:
    """All entries on file."""

    def get(self):
        """"""
        return app.view.entries(tx.pub.get_entries(), app.view.render_dict)


@app.control(r"entries/{entry}")
class Entry:
    """A single entry on file."""

    def get(self):
        """"""
        try:
            resource = tx.db.select(
                "cache", where="url = ?", vals=[f"https://{self.resource}"]
            )[0]
        except IndexError:
            resource = tx.db.select(
                "cache", where="url = ?", vals=[f"http://{self.resource}"]
            )[0]
        return app.view.cache_resource(resource)


@app.control(r"cards")
class Cards:
    """
    All cards on file.

    `OPTIONS`, `PROPFIND` and `REPORT` methods provide CardDAV support.

    """

    def get(self):
        """"""
        return app.view.cards(tx.pub.get_cards(), app.view.render_dict)

    def options(self):
        """Signal capabilities to CardDAV client."""
        web.header("DAV", "1, 2, 3, access-control, addressbook")
        web.header(
            "Allow",
            "OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, "
            "COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, "
            "UNLOCK, REPORT, ACL",
        )
        tx.response.naked = True
        return ""

    def propfind(self):
        """
        Return a status listing of addressbook/contacts.

        This resource is requsted twice with `Depth` headers of 0 and 1.
        0 is a request for the addressbook itself. 1 is a request for the
        addressbook itself and all contacts in the addressbook. Thus both
        the addressbook itself and each user have an etag.

        """
        # TODO refactor..
        web.header("DAV", "1, 2, 3, access-control, addressbook")

        depth = int(tx.request.headers["Depth"])
        etags = {"": tx.kv["carddav-lasttouch"]}
        if depth == 1:
            for identity in get_resources("identities"):
                etags[identity["-uuid"]] = identity.get(
                    "updated", identity["published"]
                ).timestamp()

        props = list(tx.request.body.iterchildren())[0]
        namespaces = set()
        responses = []

        for uuid, etag in etags.items():
            ok = []
            notfound = []
            for prop in props.iterchildren():
                # supported
                if prop.tag == "{DAV:}current-user-privilege-set":
                    ok.append(
                        """<current-user-privilege-set>
                                     <privilege>
                                         <all />
                                         <read />
                                         <write />
                                         <write-properties />
                                         <write-content />
                                     </privilege>
                                 </current-user-privilege-set>"""
                    )
                if prop.tag == "{DAV:}displayname":
                    ok.append("<displayname>carddav</displayname>")
                if prop.tag == "{DAV:}getetag":
                    ok.append(f'<getetag>"{etag}"</getetag>')
                if prop.tag == "{DAV:}owner":
                    ok.append("<owner>/</owner>")
                if prop.tag == "{DAV:}principal-URL":
                    ok.append(
                        """<principal-URL>
                                     <href>/identities</href>
                                 </principal-URL>"""
                    )
                if prop.tag == "{DAV:}principal-collection-set":
                    ok.append(
                        """<principal-collection-set>
                                     <href>/identities</href>
                                 </principal-collection-set>"""
                    )
                if prop.tag == "{DAV:}current-user-principal":
                    ok.append(
                        """<current-user-principal>
                                     <href>/identities</href>
                                 </current-user-principal>"""
                    )
                if prop.tag == "{DAV:}resourcetype":
                    namespaces.add("CR")
                    if uuid:
                        ok.append("<resourcetype />")
                    else:
                        ok.append(
                            """<resourcetype>
                                         <CR:addressbook />
                                         <collection />
                                     </resourcetype>"""
                        )
                if prop.tag == "{DAV:}supported-report-set":
                    ok.append(
                        """<supported-report-set>
                                     <supported-report>
                                         <report>principal-property-search</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>sync-collection</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>expand-property</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>principal-search-property-set</report>
                                     </supported-report>
                                 </supported-report-set>"""
                    )
                if (
                    prop.tag == "{urn:ietf:params:xml:ns:carddav}"
                    "addressbook-home-set"
                ):
                    namespaces.add("CR")
                    ok.append(
                        """<CR:addressbook-home-set>
                                     <href>/identities</href>
                                 </CR:addressbook-home-set>"""
                    )
                if prop.tag == "{http://calendarserver.org/ns/}" "getctag":
                    namespaces.add("CS")
                    ok.append(f'<CS:getctag>"{etag}"</CS:getctag>')

                # conditionally supported
                if prop.tag == "{http://calendarserver.org/ns/}me-card":
                    namespaces.add("CS")
                    if uuid:
                        notfound.append("<CS:me-card />")
                    else:
                        ok.append(
                            f"""<CS:me-card>
                                      <href>/identities/{tx.owner["-uuid"]}.vcf</href>
                                      </CS:me-card>"""
                        )

                # not supported
                if prop.tag == "{DAV:}add-member":
                    notfound.append("<add-member />")
                if prop.tag == "{DAV:}quota-available-bytes":
                    notfound.append("<quota-available-bytes />")
                if prop.tag == "{DAV:}quota-used-bytes":
                    notfound.append("<quota-used-bytes />")
                if prop.tag == "{DAV:}resource-id":
                    notfound.append("<resource-id />")
                if prop.tag == "{DAV:}sync-token":
                    notfound.append("<sync-token />")
                if prop.tag == "{urn:ietf:params:xml:ns:carddav}" "directory-gateway":
                    namespaces.add("CR")
                    notfound.append("<CR:directory-gateway />")
                if prop.tag == "{urn:ietf:params:xml:ns:carddav}" "max-image-size":
                    namespaces.add("CR")
                    notfound.append("<CR:max-image-size />")
                if prop.tag == "{urn:ietf:params:xml:ns:carddav}" "max-resource-size":
                    namespaces.add("CR")
                    notfound.append("<CR:max-resource-size />")
                if prop.tag == "{http://calendarserver.org/ns/}" "email-address-set":
                    namespaces.add("CS")
                    notfound.append("<CS:email-address-set />")
                if prop.tag == "{http://calendarserver.org/ns/}" "push-transports":
                    namespaces.add("CS")
                    notfound.append("<CS:push-transports />")
                if prop.tag == "{http://calendarserver.org/ns/}" "pushkey":
                    namespaces.add("CS")
                    notfound.append("<CS:pushkey />")
                if prop.tag == "{http://me.com/_namespace/}" "bulk-requests":
                    namespaces.add("ME")
                    notfound.append("<ME:bulk-requests />")
            href = "/identities"
            if uuid:
                href += f"/{uuid}.vcf"
            responses.append((href, ok, notfound))
        tx.response.naked = True
        raise web.MultiStatus(view.carddav(namespaces, responses))

    def report(self):
        """Return a full listing for each requested identity."""
        etags = {}
        for identity in get_resources("identities"):
            etags[identity["-uuid"]] = identity.get(
                "updated", identity["published"]
            ).timestamp()
        children = list(tx.request.body.iterchildren())
        # XXX props = children[0]  # TODO soft-code prop responses
        responses = []
        for href in children[1:]:
            uuid = href.text.rpartition("/")[2].partition(".")[0]
            ok = [
                f'<getetag>"{etags[uuid]}"</getetag>',
                f"<CR:address-data>{generate_vcard(uuid)}</CR:address-data>",
            ]
            notfound = []
            responses.append((href.text, ok, notfound))
        tx.response.naked = True
        raise web.MultiStatus(view.carddav(set(["CR"]), responses))


@app.control(r"cards/{nickname}")
class Card:
    """A single card on file."""

    def get(self):
        """"""
        # try:
        #     resource = tx.db.select("cache", where="url = ?",
        #                             vals=[f"https://{self.resource}"])[0]
        # except IndexError:
        #     resource = tx.db.select("cache", where="url = ?",
        #                             vals=[f"http://{self.resource}"])[0]
        return app.view.card(tx.pub.get_card(self.nickname))


@app.control(r"cards/{nickname}.vcf")
class VCard:
    """
    A single card on file, represented as a vCard.

    `PUT` and `DELETE` methods provide CardDAV support.

    """

    def get(self):
        """"""
        web.header("Content-Type", "text/vcard")
        return generate_vcard(self.nickname)

    def put(self):
        """
        add or update a identity

        """
        # TODO only add if "if-none-match" is found and identity isn't
        try:
            print("if-none-match", tx.request.headers.if_none_match)
        except AttributeError:
            pass
        else:
            try:
                identities.get_identity_by_uuid(self.card_id)
            except ResourceNotFound:
                pass
            else:
                raise web.Conflict("identity already exists")

        # TODO only update if "if-match" matches etag on hand
        try:
            request_etag = str(tx.request.headers.if_match).strip('"')
            print("if-match", request_etag)
        except AttributeError:
            pass
        else:
            identity = identities.get_identity_by_uuid(self.card_id)
            current_etag = identity.get("updated", identity["published"]).timestamp()
            print("current etag", current_etag)
            if request_etag != current_etag:
                raise web.Conflict("previous edit already exists")

        # TODO non-standard type-params (url) not handled by vobject

        card = vobject.readOne(tx.request.body.decode("utf-8"))

        name = card.fn.value.strip()

        extended = {}
        n = card.n.value

        def explode(key):
            item = getattr(n, key)
            if isinstance(item, list):
                extended[key] = ";".join(item)
            else:
                extended[key] = [item]

        explode("prefix")
        explode("given")
        explode("additional")
        explode("family")
        explode("suffix")

        # TODO identity_type = "identity"
        basic = {"name": name, "uuid": self.card_id}

        # TODO organizations = [o.value[0]
        # TODO                  for o in card.contents.get("org", [])]
        # TODO for organization in organizations:
        # TODO     if organization == name:
        # TODO         identity_type = "organization"

        # TODO telephones = []
        # TODO for tel in card.contents.get("tel", []):
        # TODO     telephones.append((tel.value, tel.params["TYPE"]))
        # TODO websites = []
        # TODO for url in card.contents.get("url", []):
        # TODO     type = url.params.get("TYPE", [])
        # TODO     for label in card.contents.get("x-ablabel"):
        # TODO         if label.group == url.group:
        # TODO             type.append(label.value)
        # TODO     print(url.value, type)
        # TODO     print()
        # TODO     websites.append((url.value, type))

        # photo = card.contents.get("photo")[0]
        # print()
        # print(photo)
        # print()
        # print(photo.group)
        # print(photo.params.get("ENCODING"))
        # print(photo.params.get("X-ABCROP-RECTANGLE"))
        # print(photo.params.get("TYPE", []))
        # print(len(photo.value))
        # print()
        # filepath = tempfile.mkstemp()[1]
        # with open(filepath, "wb") as fp:
        #     fp.write(photo.value)
        # photo_id = canopy.branches["images"].photos.upload(filepath)
        # extended["photos"] = [photo_id]

        try:
            details = identities.get_identity_by_uuid(self.card_id)
        except ResourceNotFound:
            print("NEW identity!")
            print(basic)
            print(extended)
            quick_draft("identity", basic, publish="Identity imported from iPhone.")
            # XXX details = create_identity(access="private", uid=self.card_id,
            # XXX                          **basic)
            # XXX details = update_identity(identifier=details["identifier"],
            # XXX                  telephones=telephones, websites=websites,
            # XXX                  **extended)
            print("CREATED")
        else:
            print("EXISTING identity!")
            print(details)
            print("UPDATED")
        # XXX     basic.update(extended)
        # XXX     details = update_identity(identifier=details["identifier"],
        # XXX                      telephones=telephones, websites=websites,
        # XXX                      **basic)
        identity = identities.get_identity_by_uuid(self.card_id)
        etag = identity.get("updated", identity["published"]).timestamp()
        web.header("ETag", f'"{etag}"')
        tx.response.naked = True
        raise web.Created("created identity", f"/identities/{self.card_id}.vcf")

    def delete(self):
        """
        delete a identity

        This method provides CardDAV support.

        """
        # delete_resource(...)
        tx.response.naked = True
        return f"""<?xml version="1.0"?>
                   <multistatus xmlns="DAV:">
                     <response>
                       <href>/identities/{self.card_id}.vcf</href>
                       <status>HTTP/1.1 200 OK</status>
                     </response>
                   </multistatus>"""


@app.control(r"rooms")
class Rooms:
    """All rooms on file."""

    def get(self):
        """"""
        return app.view.rooms(tx.pub.get_rooms(), app.view.render_dict)


@app.control(r"syndication")
class Syndication:
    """."""

    def get(self):
        """"""
        return app.view.syndication()

    def post(self):
        """"""
        destinations = web.form()
        if "twitter_username" in destinations:
            un = destinations.twitter_username
            # TODO pw = destinations.twitter_password
            # TODO sign in
            user_photo = ""  # TODO doc.qS(f"a[href=/{un}/photo] img").src
            destination = {
                "uid": f"//twitter.com/{un}",
                "name": f"{un} on Twitter",
                "service": {
                    "name": "Twitter",
                    "url": "//twitter.com",
                    "photo": "//abs.twimg.com/favicons/" "twitter.ico",
                },
                "user": {"name": un, "url": f"//twitter.com/{un}", "photo": user_photo},
            }
            tx.db.insert("syndication", destination=destination)
        if "github_username" in destinations:
            un = destinations.github_username
            # TODO token = destinations.github_token
            # TODO check the token
            user_photo = ""  # TODO doc.qS("img.avatar-user.width-full").src
            destination = {
                "uid": f"//github.com/{un}",
                "name": f"{un} on GitHub",
                "service": {
                    "name": "GitHub",
                    "url": "//github.com",
                    "photo": "//github.githubassets.com/" "favicons/favicon.png",
                },
                "user": {"name": un, "url": f"//github.com/{un}", "photo": user_photo},
            }
            tx.db.insert("syndication", destination=destination)


@app.control(r"media")
class MediaEndpoint:
    """."""

    def get(self):
        """"""
        media = tx.pub.get_media()
        try:
            query = web.form("q").q
        except web.BadRequest:
            pass
        else:
            if query == "source":
                # {
                #   "url": "https://media.aaronpk.com/2020/07/file-20200726XXX.jpg",
                #   "published": "2020-07-26T09:51:11-07:00",
                #   "mime_type": "image/jpeg"
                # }
                return {
                    "items": [
                        {
                            "url": (
                                f"{tx.request.uri.scheme}://{tx.request.uri.netloc}"
                                f"/pub/media/{filepath.name}"
                            ),
                            "published": "TODO",
                            "mime_type": "TODO",
                        }
                        for filepath in media
                    ]
                }
        return app.view.media(media)

    def post(self):
        """"""
        media_dir = pathlib.Path(tx.host.name)
        media_dir.mkdir(exist_ok=True, parents=True)
        while True:
            mid = web.nbrandom(4)
            filename = media_dir / mid
            if not filename.exists():
                filename = web.form("file").file.save(filename)
                break
        if str(filename).endswith(".heic"):
            sh.convert(
                filename,
                "-set",
                "filename:base",
                "%[basename]",
                f"{media_dir}/%[filename:base].jpg",
            )
        sha256 = str(sh.sha256sum(filename)).split()[0]
        try:
            tx.db.insert("media", mid=mid, sha256=sha256, size=filename.stat().st_size)
        except tx.db.IntegrityError:
            mid = tx.db.select("media", where="sha256 = ?", vals=[sha256])[0]["mid"]
            filename.unlink()
        path = f"/pub/media/{mid}"
        raise web.Created(f"File can be found at <a href={path}>{path}</a>", path)


@app.control(r"media/{filename}")
class MediaFile:
    """."""

    def get(self):
        """"""
        content_types = {
            (".jpg", ".jpeg"): "image/jpg",
            ".heic": "image/heic",
            ".png": "image/png",
            ".mp3": "audio/mpeg",
            ".mov": "video/quicktime",
            ".mp4": "video/mp4",
        }
        for suffix, content_type in content_types.items():
            if self.filename.endswith(suffix):
                web.header("Content-Type", content_type)
                break
        relative_path = f"{tx.host.name}/{self.filename}"
        if tx.host.server[0] == "gunicorn":
            with open(relative_path, "rb") as fp:
                return fp.read()
        else:  # assumes Nginx context
            web.header("X-Accel-Redirect", f"/X/{relative_path}")

    def delete(self):
        """"""
        filepath = tx.pub.get_filepath(self.filename)
        tx.db.delete("media", where="mid = ?", vals=[filepath.stem])
        filepath.unlink()
        return "deleted"
