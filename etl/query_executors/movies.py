def query_get_movies(last_time, limit, offset) -> str:
    return f"""
        SELECT 
            fw.id, 
            fw.title, 
            fw.description, 
            fw.updated_at,  
            fw.created_at
        FROM content.filmwork fw
        WHERE fw.updated_at > '{last_time}'
        GROUP BY fw.id
        LIMIT {limit} OFFSET {offset}; 
    """