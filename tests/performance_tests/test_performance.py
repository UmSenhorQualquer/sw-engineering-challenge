from concurrent.futures import ProcessPoolExecutor
import time
import requests
import statistics
from tabulate import tabulate

BASE_URL = "http://localhost:8000"  # API URL

NUMBER_REQUESTS = 1000  # Total number of requests per test
CONCURRENCY_LEVELS = [1, 5, 10, 20, 50, 100]  # Number of concurrent workers
    

def make_request(endpoint):
    """
    Make a single request to the specified endpoint.
    """
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/{endpoint}")
        end_time = time.time()
        return end_time - start_time, response.status_code
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def run_concurrent_requests(endpoint, num_requests, num_workers):
    """
    Run concurrent requests using multiprocessing.
    """
    start_time_total = time.time()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(make_request, endpoint) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    end_time_total = time.time()
    total_time = end_time_total - start_time_total
    
    # Filter out failed requests
    successful_results = [r[0] for r in results if r[0] is not None]
    
    if not successful_results:
        return {
            'min': None,
            'max': None,
            'mean': None,
            'median': None,
            'total_requests': num_requests,
            'successful_requests': 0,
            'failed_requests': num_requests,
            'requests_per_second': 0
        }
    
    return {
        'min': min(successful_results),
        'max': max(successful_results),
        'mean': statistics.mean(successful_results),
        'median': statistics.median(successful_results),
        'total_requests': num_requests,
        'successful_requests': len(successful_results),
        'failed_requests': num_requests - len(successful_results),
        'requests_per_second': len(successful_results) / total_time
    }

def test_api_performance():
    """
    Test the API performance with different concurrency levels.
    """
    endpoints = [
        "bloqs/",
        "bloqs/22ffa3c5-3a3d-4f71-81f1-cac18ffbc510",
        "lockers/",
        "lockers/2191e1b5-99c7-45df-8302-998be394be48",
        "rents/",
        "rents/feb72a9a-258d-49c9-92de-f90b1f11984d",
    ]
    
    print("\nAPI Performance Test Results:")
    print("=" * 80)
    
    for endpoint in endpoints:
        print(f"\nTesting endpoint: /{endpoint}")
        print("-" * 40)
        
        # Prepare table data
        table_data = []
        headers = ["Workers", "Total Reqs", "Successful", "Failed", "Reqs/sec", "Min (s)", "Max (s)", "Mean (s)", "Median (s)"]
        
        for num_workers in CONCURRENCY_LEVELS:
            print(f"Running tests with {num_workers} workers...")
            results = run_concurrent_requests(endpoint, NUMBER_REQUESTS, num_workers)
            
            if results['mean'] is None:
                row = [num_workers, NUMBER_REQUESTS, 0, NUMBER_REQUESTS, 0, "N/A", "N/A", "N/A", "N/A"]
            else:
                row = [
                    num_workers,
                    results['total_requests'],
                    results['successful_requests'],
                    results['failed_requests'],
                    f"{results['requests_per_second']:.2f}",
                    f"{results['min']:.4f}",
                    f"{results['max']:.4f}",
                    f"{results['mean']:.4f}",
                    f"{results['median']:.4f}"
                ]
            table_data.append(row)
        
        # Print the table
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print("\n")

if __name__ == "__main__":
    test_api_performance()
