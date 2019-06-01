from setuptools import setup

setup(
    name="reviews-platzi",
    version="0.1.9",
    description="A script to get all the reviews from one Platzi course",
    author="Kevin Morales",
    author_email="kenshumorales@gmail.com",
    packages=["reviews_platzi"],
    install_requires=["requests", "beautifulsoup4"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["rplatzi=reviews_platzi.rplatzi:main"]},
)
