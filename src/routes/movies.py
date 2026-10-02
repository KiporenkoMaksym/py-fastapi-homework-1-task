from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import MovieModel
from src.schemas import movies
from src.database import get_db


router = APIRouter()

@router.get("/movies/", response_model=movies.MovieListResponseSchema)
async def get_movies(
    page: int = Query(default=1, ge=1, description="The page number to fetch."),
    per_page: int = Query(default=10, ge=1, le=20, description="Number of movies per page."),
):
    total_items = 9999
    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages and total_items > 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    base_url = "/api/v1/theater/movies/"
    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    movies = [
        {
            "id": 1,
            "name": "Creed III",
            "date": "2023-03-02",
            "score": 73,
            "genre": "Drama,Action",
            "overview": "After dominating the boxing world...",
            "crew": "Michael B. Jordan, Tessa Thompson",
            "orig_title": "Creed III",
            "status": "Released",
            "orig_lang": "English",
            "budget": 75000000,
            "revenue": 271616668,
            "country": "AU",
        }
    ]

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

@router.get("/movies/{movie_id}", response_model=movies.MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))

    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Movie with the given ID was not found"
        )

    return movie
