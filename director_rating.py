import os
from bs4 import BeautifulSoup

def extract_ratings_from_imdb(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")

    movies = []
    for item in soup.find_all("li", {"class": "ipc-metadata-list-summary-item"}):
        rating_tag = item.find("span", {"class": "ipc-rating-star--rating"})
        if rating_tag:
            rating = float(rating_tag.get_text(strip=True))
            movies.append(rating)

    average_rating = sum(movies) / len(movies) if movies else None
    return average_rating


if __name__ == "__main__":
    folder_path = "."  

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            director_name = os.path.splitext(file_name)[0] 
            file_path = os.path.join(folder_path, file_name)

            avg = extract_ratings_from_imdb(file_path)
            if avg:
                print(f"{director_name}: {avg:.2f}")
            else:
                print(f"{director_name}: No ratings found")
