import time


def time_function(pipeline_stage: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("")
            print(f"{pipeline_stage}...")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"{pipeline_stage} completed in {elapsed_time:.4f} seconds.")
            print("")
            return result

        return wrapper

    return decorator
