# YouTube Trailer Sentiment vs IMDb Ratings

**CPSC 368 – Project Group 9**  
Min Cho · Edward Kim · Edward Kim · Daniel Park · Annabel Lim

---

## Overview

This project examines whether audience sentiment toward movie trailers on YouTube (comments, likes, dislikes, and engagement) is related to IMDb movie ratings. We investigate whether early audience reactions to trailers reflect how viewers ultimately rate the movie.

---

## Research Questions

- Does the relationship between trailer sentiment and IMDb rating differ by genre?
- Do positive vs negative comment ratios differ between high-rated and low-rated movies?
- Can YouTube sentiment and engagement metrics predict IMDb ratings?

---

## Data Sources

**IMDb datasets (movie metadata and ratings)**  
[https://datasets.imdbws.com](https://datasets.imdbws.com)

**YouTube trailer sentiment dataset**  
[https://www.kaggle.com/datasets/dineshvasired/movies-youtube-trailers-and-sentiment](https://www.kaggle.com/datasets/dineshvasired/movies-youtube-trailers-and-sentiment)


## Repository Structure

```
.
├── data
│   ├── raw/        raw datasets
│   └── cleaned/    cleaned datasets
│
├── notebooks
│   └── exploration.ipynb
│
├── src
│   ├── load_data.py
│   ├── clean_data.py
│   └── transform_features.py
│
└── README.md
```

---

## Collaboration Workflow

To keep the repository organized and avoid merge conflicts, each team member works on their own branch.

1. Switch to your personal branch.
2. Make changes and commit your work to your branch.
3. Push your branch to GitHub.
4. Open a **Pull Request** to merge your changes into the `main` branch.
5. After review, the changes are merged into `main`.

This workflow ensures that each member can work independently while keeping the main branch stable.