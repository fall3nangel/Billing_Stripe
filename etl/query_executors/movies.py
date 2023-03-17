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


def query_get_products(last_time, limit, offset) -> str:
    return f"""
        SELECT 
            p.id, 
            p.name, 
            p.price, 
            p.duration, 
            p.updated_at,  
            p.created_at
        FROM content.product p
        WHERE p.updated_at > '{last_time}'
        GROUP BY p.id
        LIMIT {limit} OFFSET {offset}; 
    """


def query_get_product_movie_pairs(last_time, limit, offset) -> str:
    return f"""
        SELECT 
            fwp.id, 
            fwp.filmwork_id, 
            fwp.product_id
        FROM content.filmwork_product fwp
        WHERE fwp.updated_at > '{last_time}'
        GROUP BY fwp.id
        LIMIT {limit} OFFSET {offset}; 
    """
