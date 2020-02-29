import requests
import time

headers = {"Authorization": "token ######"}

initial = "null"
results = [] #vetor de resultados

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    while (request.status_code == 502):
          time.sleep(2)
          request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query falhou! Codigo de retorno: {}. {}".format(request.status_code, query))

for x in range(50):        
      query = """
      {
        search(query:"stars:>100", type:REPOSITORY, first:20, after:%s){
          nodes{
            ... on Repository
            {
              nameWithOwner
              url
              primaryLanguage
              {
                name
              }
              acceptedPullRequests: pullRequests(states:MERGED)
              {
                totalCount
              }
              releases
              {
                totalCount
              }
              closedIssues: issues(states:CLOSED)
              {
                totalCount
              }
              totalIssues: issues
              {
                totalCount
              }
              createdAt
              updatedAt
            }
          }
          pageInfo
          {
            endCursor
          }
        }
      }
      """ % (initial)

      result = run_query(query)
      for y in range(20):
        results.append(result["data"]["search"]["nodes"][y])
      initial = '"{}"'.format(result["data"]["search"]["pageInfo"]["endCursor"])

print(results)