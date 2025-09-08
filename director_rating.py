import os
import csv
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
    folder_path = "./2024"
    director_list_path = "./2024/directorlist.txt"
    output_csv = "director_ratings_2024.csv"

    with open(director_list_path, "r", encoding="utf-8") as f:
        directors = [line.strip() for line in f if line.strip()]

    results = []

    for director_name in directors:
        file_path = os.path.join(folder_path, f"{director_name}.txt")
        if os.path.exists(file_path):
            avg = extract_ratings_from_imdb(file_path)
            results.append({
                "Director": director_name,
                "Average Rating": f"{avg:.2f}" if avg else "No ratings found"
            })
        else:
            results.append({
                "Director": director_name,
                "Average Rating": "File not found"
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Director", "Average Rating"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved in {output_csv}")
