import urllib.request, json, ssl
import pickle

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class Node:
    def __init__(self, domain, seller_type, children):
        self.domain = domain
        self.seller_type = seller_type
        self.children = children


all_domains = {}
tree = Node("openx.com", "intermediary", {})

to_do = 1
done = 0


def load(domain, root_path):
    global done
    global to_do

    node = tree
    for i in root_path:
        node = node.children[i]

    url = "https://" + domain + "/sellers.json"

    print(f"{done}/{to_do} ({(done / to_do) * 100}%)")

    try:
        all_domains[domain] = True
        data = None
        with urllib.request.urlopen(url, context=ctx) as urll:
            data = json.loads(urll.read().decode())

        for i in filter(lambda i: i["seller_type"].lower() == "publisher", data["sellers"]):
            node.children[i["domain"].lower()] = Node(i["domain"].lower(), "publisher", None)

        intermediaries = list(
            filter(lambda i: i["seller_type"].lower() == "intermediary" or i["seller_type"].lower() == "both", data["sellers"]))

        for i in intermediaries:
            node.children[i["domain"].lower()] = Node(i["domain"].lower(), i["seller_type"].lower(), {})

        unique = list(set(map(lambda i: i["domain"].lower(), intermediaries)))
        unique_not_repeated_domains = list(filter(lambda i: i not in all_domains, unique))

        to_do += len(unique_not_repeated_domains)

        for domain in unique_not_repeated_domains:
            load(domain, root_path + [domain])
        return
    except Exception as e:
        pass
    finally:
        done += 1


load("openx.com", [])

with open('filename2.pickle', 'wb') as handle:
    pickle.dump(tree, handle, protocol=pickle.HIGHEST_PROTOCOL)
