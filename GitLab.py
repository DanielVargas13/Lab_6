import requests
import time

headers = {"Authorization": "token 9447a02281c83005f5d9858dd675b86cbb5aa340"}

initial = "null"

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    while (request.status_code == 502):
          time.sleep(2)
          request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query falhou! Codigo de retorno: {}. {}".format(request.status_code, query))

for x in range(5):        
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
      print(result)
      initial = '"{}"'.format(result["data"]["search"]["pageInfo"]["endCursor"])