from .schemes import PageResponseModel


async def paginate(page, query, scheme_converter, limit):
    paginated_query = query.offset((page - 1) * limit).limit(limit).all()
    return PageResponseModel(
        total=query.count(),
        page=page,
        size=limit,
        results=[await scheme_converter(item) for item in paginated_query]
    )
