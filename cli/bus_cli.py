from backend.loader import load_bus_routes
from backend.routing import find_route
from backend.translator import t

routes = load_bus_routes()

def main():
    lang = input("Language (en/mm/th): ").strip()
    if lang not in ["en", "mm", "th"]:
        lang = "en"

    print(t("title", lang))

    while True:
        print("1) Search bus\n2) Suggest route\n3) Exit")
        c = input("> ")

        if c == "1":
            num = input(t("enter_bus", lang))
            if num in routes:
                print(routes[num])
            else:
                print(t("not_found", lang))

        elif c == "2":
            s = input(t("from", lang))
            e = input(t("to", lang))
            res = find_route(routes, s, e)
            print(res or t("none", lang))

        else:
            break

if __name__ == "__main__":
    main()
