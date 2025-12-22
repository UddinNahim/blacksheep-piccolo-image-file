import datetime
from typing import Literal
from blacksheep import FromQuery, Response,json,status_code , not_found ,Request ,no_content
from blacksheep.server.controllers import get,post,put,delete ,patch
from app.tables import Course
from piccolo.engine import Engine
from typing  import Literal ,Optional





@post("/courses")
async def create_course(request):
    try:
        data = await request.json()
        course = Course(**data)
        await course.save()
        return json(course.to_dict())
    except Exception as e:
        return json({"error":str(e)},status=400)

#GET ALL Courses
@get("/courses")
async def get_courses():
    courses = await Course.select()
    return json(courses)

#single Course

@get("/courses/{id}")
async def single_course(id:int):
   try:
        course = await Course.select().where(Course.id == id).first()
        if course is None:
            return not_found({"message":f"Course with id {id} not found"})
        return course
   except Exception as e:
       return json({"error": str(e)},status = 400)


#update course
#  UPDATE course SET rating = 5.0 WHERE id = 1;
# await Course.update({Course.rating: 5.0}).where(Course.id == id)

@patch("/courses/{id}")
async def update_course(id:int, request:Request):
    data = await request.json()
    try:
         # Ensure the course exists
        await Course.objects().get(Course.id == id)
         # Perform update
        await( Course.update(data).where(Course.id == id).run())

        #fetch updated record
        updated_course = await Course.objects().get(Course.id == id)
        return json(updated_course.to_dict())
    except Exception as e:
        return json({"error": str(e)},status = 400)
    
@delete("/courses/{id}")
async def delete_course(id: int):
    exists = (
        await Course
        .select(Course.id)
        .where(Course.id == id)
        .first()
    )

    if not exists:
        return Response(404)

    await Course.delete().where(Course.id == id).run()
    return Response(204)


#GET ALL Courses

from typing import Optional, Literal
from blacksheep import json
from blacksheep.server.controllers import get
from app.tables import Course

from typing import Optional, Literal
from blacksheep import json, get # Corrected import
from app.tables import Course

from blacksheep import get, json # Import get directly
from app.tables import Course
from datetime import datetime

@get("/all_courses")
async def get_courses(
    min_price: float = None,
    max_price: float = None,
    min_rating: float = None,
    max_rating: float = None,
    start_date: FromQuery[datetime] = None, # Matches your API param name
    end_date: FromQuery[datetime] = None,   # Matches your API param name
    sort_by: str = "name", 
    order: str = "asc",
    search: str = None
):
    query = Course.select()

    # 1. Price Filtering
    if min_price is not None:
        query = query.where(Course.price >= min_price)
    if max_price is not None:
        query = query.where(Course.price <= max_price)

    # 2. Rating Filtering
    if min_rating is not None:
        query = query.where(Course.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Course.rating <= max_rating)

    # 3. Datetime Filtering (Fixed column name to 'create')
    if start_date:
        query = query.where(Course.create >= start_date.value)
    if end_date:
        # from datetime import timedelta
        # adjusted_end = end_date.value + timedelta(seconds=1)
        # query = query.where(Course.create < adjusted_end)
        query = query.where(Course.create <= end_date.value)

    # 4. Searching 
    if search:
        query = query.where(
            (Course.name.ilike(f'%{search}%')) | 
            (Course.description.ilike(f"%{search}%"))
        )

    # 5. Sorting
    sort_column_map = {
        "name": Course.name,
        "rating": Course.rating,
        "price": Course.price,
        "create": Course.create
    }
    
    sort_by = sort_by if sort_by in sort_column_map else "name"
    query = query.order_by(sort_column_map[sort_by], ascending=(order == "asc"))

    courses = await query.run()
    return json(courses)

# @post("/courses")
# async def create_course(request):
#     try:
#         data = await request.json()
#         course = Course(**data)
#         await course.save()
#         return json(course.to_dict())
#     except Exception as e:
#         return json({"error":str(e)},status=400)





