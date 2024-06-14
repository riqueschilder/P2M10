from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()

blog_posts = []

class BlogPost(BaseModel):
    id: int
    title: str
    content: str

# Setup logging
logging.basicConfig(filename='app.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

@app.post('/blog', status_code=201)
async def create_blog_post(post: BlogPost):
    try:
        blog_posts.append(post)
        logging.warning(f"Blog post created: {post}")
        return {'status':'success'}
    except KeyError:
        logging.error("Invalid request data")
        raise HTTPException(status_code=400, detail='Invalid request')
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/blog')
async def get_blog_posts():
    return {'posts': [post.dict() for post in blog_posts]}

@app.get('/blog/{id}')
async def get_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            return {'post': post.dict()}
    logging.warning(f"Blog post not found: {id}")
    raise HTTPException(status_code=404, detail='Post not found')

@app.delete('/blog/{id}')
async def delete_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logging.warning(f"Blog post deleted: {id}")
            return {'status':'success'}
    logging.warning(f"Blog post not found for deletion: {id}")
    raise HTTPException(status_code=404, detail='Post not found')

@app.put('/blog/{id}')
async def update_blog_post(id: int, updated_post: BlogPost):
    try:
        for post in blog_posts:
            if post.id == id:
                post.title = updated_post.title
                post.content = updated_post.content
                logging.warning(f"Blog post updated: {post}")
                return {'status':'success'}
        logging.warning(f"Blog post not found for update: {id}")
        raise HTTPException(status_code=404, detail='Post not found')
    except KeyError:
        logging.error("Invalid request data")
        raise HTTPException(status_code=400, detail='Invalid request')
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
