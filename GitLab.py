import requests

headers = {"Authorization": "token a2899f94ada7b3da849e42ad0a1980f6985cbd9a"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query falhou! Codigo de retorno: {}. {}".format(request.status_code, query))

               
query = """
{
  search(query:"stars:>100", type:REPOSITORY, first:100){
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
  }
}
"""

result = run_query(query)
print(result)