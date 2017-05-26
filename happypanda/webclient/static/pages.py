__pragma__ ('alias', 'S', '$') # JQuery

from client import client, Base
import utils

class BasePage(Base):
    
    def main(self):
        ""
        self.get_mode()
        self.get_versions()

    def get_versions(self, data=None, error=None):
        ""
        lbl = self.get_label('default')
        vs = [
            ('server', 'unknown'),
            ('webclient', 'unknown'),
            ('database', 'unknown'),
            ('torrent client', 'unknown'),
            ]

        if data and not error:
            vs = []
            lbl = self.get_label('info')
            vs.append(('server', ".".join(str(x) for x in data['core'])))
            vs.append(('webclient', ".".join(str(x) for x in data['web'])))
            vs.append(('database', ".".join(str(x) for x in data['db'])))
            vs.append(('torrent client', ".".join(str(x) for x in data['torrent'])))
        elif error:
            pass
        else:
            client.call_func("get_version", self.get_versions)

        for k in vs:
            self.compile("#footer-right-t", "#footer-right", append=True, key=k[0], value=k[1], label=lbl)


    def get_mode(self, data=None, error=None):
        ""
        txt = "unknown"
        lbl = "default"
        if data and not error:
            lbl = "info"
            if data["core.debug"] and data["core.preview"] :
                txt = "preview debug"
            elif data["core.debug"] :
                txt = "debug"
            elif data["core.preview"] :
                txt = "preview"
            else:
                txt = "normal"
        elif error:
            pass
        else:
            client.call_func("get_settings", self.get_mode, settings=["core.debug", "core.preview"])

        self.compile("#footer-right-t", "#footer-right", key="mode", value=txt, label=self.get_label(lbl))

base = BasePage()

class ApiPage(Base):

    def call(self):
        func_args = {}
        def each_d(index, element):
            lichildren = S(this).children()
            key = lichildren.eq(0).find("input").val()
            value = lichildren.eq(1).find("input").val()
            if key and value:
                value = value.strip()
                if value.startswith('[') and value.endswith(']'):
                    value = [x.strip() for x in value.replace('[', '').replace(']', '').split(',') if x]
                func_args[key] = value
        S("div#args > ul > li").each(each_d)
        f_dict = {
            'fname': S("#fname").val()
            }
        f_dict.update(func_args)
        client.call(
            [f_dict],
            lambda msg: S("pre#json-receive").html(utils.syntax_highlight(JSON.stringify(msg, None, 4))))
        S("pre#json-send").html(utils.syntax_highlight(JSON.stringify(client._last_msg, None, 4)))

    def add_kwarg(self):
        S("div#args > ul").append(
            """
            <li>
            <div class='col-xs-6'>
            <input type='text', placeholder='keyword' class='form-control'>
            </div>
            <div class='col-xs-6'>
            <input type='text', placeholder='value' class='form-control'>
            </div>
            </li>
            """)

api = ApiPage()

class LibraryPage(Base):

    def __init__(self, name="Library", url="/library"):
        super().__init__(url)
        self.name = name
        self.grid = None
        self.artists = {} # id : artist obj
        self.tags = {} # ns : tag
        self.glists = {} # id : list obj
        self.item_limit = 50
        self._page_limit = 10
        self._page_list = []

        self.reset_context()
    def context_nav(self, *args):
        """
        Insert a breadcumb element
        Pass tuples of (name, url)
        """

        ctx_links = [{'name': x[0], 'url': x[1]} for x in args]

        self.compile("#context-nav-t", "#content", before=True, context_links=ctx_links)


    def add_context(self, name, url):
        self._context_link.append((name, url))

    def reset_context(self):
        self._context_link = [(self.name, self.url)]

    def main(self):
        self.fetch_glists()
        self.context_nav(*self._context_link)
        self.show_pagination()

    __pragma__('iconv')
    __pragma__ ('kwargs')
    def update_sidebar(self, lists=None, tags=None, artist_obj={}):
        ""
        
        if artist_obj is not None:
            artist_data = []
            for a in artist_obj:
                artist_data.append({'name':artist_obj[a]['name'], 'count':artist_obj[a]['count']})
            self.compile("#side-artists-t", "#side-artists .list-group", append=True, side_artists=artist_data)
    __pragma__ ('nokwargs')
    __pragma__('noiconv')

    def update_pagination(self, from_page=1):
        ""

        back_disabled = False
        next_disabled = False

        if from_page - 1 == 0:
            back_disabled = True

        if from_page == len(self._page_list):
            next_disabled = True

        half_limit = int(self._page_limit/2)
        l_index = from_page-half_limit
        r_index = from_page+half_limit + 1
        if r_index > len(self._page_list):
            r_index = len(self._page_list)
            l_index = len(self._page_list) - (self._page_limit + 1)

        if l_index < 0:
            l_index = 0
            r_index = self._page_limit
        current_pages = self._page_list[l_index:r_index]

        pages = []

        for n in current_pages:
            pages.append({'number':n, 'active':n == from_page})

        self.show_items(page=from_page)

        self.compile("#item-pagination-t", ".item-pagination",
                     pages=pages,
                     back_disabled=back_disabled,
                     next_disabled=next_disabled,
                     back_number=from_page-1,
                     next_number=from_page+1)

    def show_pagination(self, data=None, error=None):
        ""
        if data and not error:
            pages = data['count']/self.item_limit
            if pages < 1:
                pages = 1
            # check if number is whole
            if pages % 1 == 0: # Note: will fail on very large numbers eg. 999999999999999999999
                pages = int(pages) + 1
            else:
                pages = int(pages)
            self._page_list = range(1, pages+1)
            self.update_pagination()
        elif error:
            pass
        else:
            client.call_func("get_count", self.show_pagination, item_type='Gallery')

    def fetch_glists(self, data=None, error=None):
        ""
        if data and not error:
            lists_data = []
            for gl in data:
                self.glists[gl['id']] = gl
                lists_data.append({'name':gl['name']})

            self.compile("#side-lists-t", "#side-lists .list-group", append=True, side_lists=lists_data)
        elif error:
            pass
        else:
            client.call_func("get_glists", self.fetch_glists)

    __pragma__('iconv')
    __pragma__ ('kwargs')
    def show_items(self, data=None, error=None, page=1):
        if data and not error:
            items = []
            for g in data:
                for a in g['artists']:
                    a_id = a['id']
                    if a_id in self.artists:
                        self.artists[a_id]['count'] += 1
                    else:
                        self.artists[a_id] = a
                        self.artists[a_id]['count'] = 1

                items.append({
                    'title': g['titles'][0]['name'],
                    'artist': g['artists'][0]['name'],
                    })

            self.update_sidebar(artist_obj=self.artists)
            self.compile("#items-t", "#items", **{'items':items})

            self.grid = __new__(Minigrid({
                'container': '.grid-items',
                'item' : '.grid-item',
                'gutter': 10
                }))
            self.grid.mount()
        elif error:
            pass
        else:
            client.call_func("library_view", self.show_items,
                             limit=self.item_limit,
                             page=page-1
                             )
    __pragma__('noiconv')
    __pragma__ ('nokwargs')


library = LibraryPage()

def init():
    S('div[onload]').trigger('onload')

    window.addEventListener('resize', lambda: library.grid.mount() if library.grid else None)

S(document).ready(init)