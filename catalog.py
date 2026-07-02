import json

# 🔹 Load data
def load_catalog():
    with open("data/shl_catalog.json", "r", encoding="utf-8") as file:
        return json.load(file)


# 🔹 Process user query (clean input)
def process_query(query):
    query = query.lower().strip()

    stop_words = ["for", "a", "an", "the", "role", "job"]
    words = query.split()

    keywords = [w for w in words if w not in stop_words]

    return keywords


# 🔹 Smart recommendation system
def recommend_assessments(query):
    catalog = load_catalog()
    keywords = process_query(query)

    results = []

    for item in catalog:
        name = item.get("name", "").lower()
        description = item.get("description", "").lower()

        score = 0

        for word in keywords:
            if word in name:
                score += 4
            if word in description:
                score += 2

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])

    return [item for score, item in results]


# 🔹 MAIN CHATBOT LOOP
if __name__ == "__main__":
    print("🤖 SHL Assessment Recommender")
    print("Type a role or skill (or type 'exit' to quit)\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            print("Goodbye 👋")
            break

        matches = recommend_assessments(query)

        print("\n🤖 Top Recommendations:\n")

        if not matches:
            print("No results found. Try different keywords.\n")
            continue

        for m in matches[:5]:
            print("-", m.get("name"))
            print("  Duration:", m.get("duration"))
            print("  URL:", m.get("url"))
            print()

        print("-" * 40)

def search_assessments(query):
    return recommend_assessments(query)