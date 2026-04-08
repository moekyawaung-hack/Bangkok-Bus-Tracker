from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import webbrowser

from backend.loader import load_bus_routes
from backend.routing import find_route
from backend.translator import t
from backend.map_routing import build_google_maps_url

routes = load_bus_routes()

KV = """
ScreenManager:
    HomeScreen:
    SearchScreen:
    RouteDetailScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: app.tr("title")
            font_size: 28
        Button:
            text: app.tr("search_route")
            size_hint_y: None
            height: 60
            on_release: app.root.current = "search"

<SearchScreen>:
    name: "search"
    BoxLayout:
        orientation: "vertical"
        TextInput:
            id: start
            hint_text: app.tr("from")
        TextInput:
            id: end
            hint_text: app.tr("to")
        Button:
            text: app.tr("find")
            size_hint_y: None
            height: 60
            on_release: app.search_route(start.text, end.text)

<RouteDetailScreen>:
    name: "detail"
    BoxLayout:
        orientation: "vertical"
        Label:
            id: result
            text: ""
        Button:
            text: "Open in Google Maps"
            size_hint_y: None
            height: 60
            on_release: app.open_first_route_map()
        Button:
            text: "Back"
            size_hint_y: None
            height: 60
            on_release: app.root.current = "search"
"""

class HomeScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

class RouteDetailScreen(Screen):
    pass

class BusApp(App):
    lang = "en"
    last_route = None

    def tr(self, key):
        return t(key, self.lang)

    def build(self):
        return Builder.load_string(KV)

    def search_route(self, start, end):
        res = find_route(routes, start, end)
        detail = self.root.get_screen("detail").ids.result
        if not res:
            detail.text = self.tr("no_route")
            self.last_route = None
        else:
            detail.text = "\n".join([f"{r['bus']} - {r['name']}" for r in res])
            self.last_route = res[0]
        self.root.current = "detail"

    def open_first_route_map(self):
        if not self.last_route:
            return
        bus_num = self.last_route["bus"]
        route = routes[bus_num]
        start_id = route["stops"][0]
        end_id = route["stops"][-1]
        url = build_google_maps_url(start_id, end_id)
        webbrowser.open(url)

if __name__ == "__main__":
    BusApp().run()
