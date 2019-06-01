import csv
import requests
from bs4 import BeautifulSoup


def main(url_course, pages):

    with open(f"reviews-{url_course}.csv", "w") as f:
        writer = csv.writer(f, delimiter=",")

        writer.writerow(["stars", "name", "content-review"])

        for page in range(1, pages + 1):
            URL = f"https://platzi.com/cursos/{url_course}/opiniones/{page}/"

            r = requests.get(URL)
            soup = BeautifulSoup(r.text, "html.parser")

            review_description = soup.find_all("div", {"class": "Review"})

            for reviews in review_description:
                review = reviews.find(
                    "div", attrs={"class": "Review-description"}
                ).text.strip()

                name_reviewer = reviews.find(
                    "div", attrs={"class": "Review-name"}
                ).text.strip()

                stars = reviews.find("div", attrs={"class": "Review-stars"})
                star = len(stars.find_all("i", "fulled"))

                writer.writerow([star, name_reviewer, review])

        print("Listo, ya puedes revisar las reviews de este curso en el csv.")


if __name__ == "__main__":
    url_course = input("¿Cuál es la URL del curso?: ")
    pages = int(input("¿Cuántas páginas de reviews tiene el curso?: "))

    main(url_course, pages)
