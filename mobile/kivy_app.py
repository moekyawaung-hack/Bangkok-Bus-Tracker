from kivy.app import App
from kivy.lang import Builder
from backend.loader import load_bus_routes
from backend.routing import find_route
from backend.translator import t

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
            font_size: 32
        Button:
            text: app.tr("search_route")
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
            on_release: app.search_route(start.text, end.text)

<RouteDetailScreen>:
    name: "detail"
    BoxLayout:
        orientation: "vertical"
        Label:
            id: result
            text: ""
"""

class HomeScreen:
    pass

class SearchScreen:
    pass

class RouteDetailScreen:
    pass

class BusApp(App):
    lang = "en"

    def tr(self, key):
        return t(key, self.lang)

    def build(self):
        return Builder.load_string(KV)

    def search_route(self, start, end):
        res = find_route(routes, start, end)
        detail = self.root.get_screen("detail").ids.result
        if not res:
            detail.text = self.tr("no_route")
        else:
            detail.text = "\n".join([f"{r['bus']} - {r['name']}" for r in res])
        self.root.current = "detail"

if __name__ == "__main__":
    BusApp().run()
