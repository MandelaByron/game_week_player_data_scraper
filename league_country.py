from operator import imod
import requests
import json
import pycountry

def league_country(slug):
    url = "https://api.sorare.com/graphql"

    payload = {
        "operationName": "LeagueQuery",
        "variables": {"slug": f"{slug}"},
        "extensions": {"operationId": "React/93339f96126979d5e1f9649952142e4f2aa25335a7a73a788f3a346407d0ab47"}
    }
    headers = {
        "cookie": "_gcl_au=1.1.1890297955.1663001791; _rdt_uuid=1663001791814.ea5e9cc3-7182-4730-8236-2368b39162d8; _fbp=fb.1.1663001792290.1052334442; _tt_enable_cookie=1; _ttp=c93822ae-3745-4026-8d5d-215e3abf19c5; ajs_anonymous_id=809ace57-6dcc-49a1-97f1-300ec1f6c698; _hjSessionUser_1730436=eyJpZCI6IjAyNmNhNjNlLWJlOTUtNTMwYS1iYjg0LTQ5OTU4OTIwNjk5MyIsImNyZWF0ZWQiOjE2NjMwMDE3OTE3NTAsImV4aXN0aW5nIjp0cnVlfQ==; ajs_user_id=cadbfe63-f205-4b39-b252-df109bf063e4; csrftoken=UGSQc%2FgxFIcFNqsspoURsYbl9xhLRGLLxSrzwmOeklnztMtx3g6LPpHYNybgeXFi3aYt3MxAZXR9nC6g2EHCYA%3D%3D; amplitude_idundefinedsorare.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _gcl_aw=GCL.1663484411.CjwKCAjw4JWZBhApEiwAtJUN0CvfK1rMQf4hmamrtmG3h97gREX0h5Rg1_5LJbQlks6TL8r1gczsQRoCHLMQAvD_BwE; _hjSession_1730436=eyJpZCI6ImM3YmQwOTVkLTM0ZGEtNGRkYS04YjliLWMwMjY4ODA0NjYxZCIsImNyZWF0ZWQiOjE2NjM0ODQ0MTk4ODQsImluU2FtcGxlIjp0cnVlfQ==; _gid=GA1.2.986780372.1663484424; _gac_UA-127797496-1=1.1663484424.CjwKCAjw4JWZBhApEiwAtJUN0CvfK1rMQf4hmamrtmG3h97gREX0h5Rg1_5LJbQlks6TL8r1gczsQRoCHLMQAvD_BwE; ab.storage.deviceId.f9062f4a-69b2-4d6b-a39c-23bc77cf4004=%7B%22g%22%3A%2260ff5344-5ab7-40cf-8d9b-696fcefa1d0d%22%2C%22c%22%3A1663001861517%2C%22l%22%3A1663484520591%7D; ab.storage.userId.f9062f4a-69b2-4d6b-a39c-23bc77cf4004=%7B%22g%22%3A%22User%3Acadbfe63-f205-4b39-b252-df109bf063e4%22%2C%22c%22%3A1663001861507%2C%22l%22%3A1663484520592%7D; _gat_UA-127797496-1=1; _ga_1DHGT9FK62=GS1.1.1663484417.3.1.1663485143.0.0.0; amplitude_id_344e75d91d2c6d4a2f468ec9c6b7abecsorare.com=eyJkZXZpY2VJZCI6ImM1YzMyMDU5LTQ0ZTEtNGU1My04ZWFhLTk4OGUyMDVkMmE4Y1IiLCJ1c2VySWQiOiJjYWRiZmU2My1mMjA1LTRiMzktYjI1Mi1kZjEwOWJmMDYzZTQiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2NjM0ODQ0MDU3NTAsImxhc3RFdmVudFRpbWUiOjE2NjM0ODUxNDg0OTksImV2ZW50SWQiOjgsImlkZW50aWZ5SWQiOjIwLCJzZXF1ZW5jZU51bWJlciI6Mjh9; _sorare_session_id=838t2%2BNblb63ooqpUEKJ8W1ycOkQdZ5uBMB75W1U7myWsPcZax2Kcph%2F01SXqbOt1rm1njgfvx5aqMHpaoeOQmxTmKKOBaGTha9IcKhUwYgixQZranljLn4UEjuiMSwHiJK2qXUSWFfMOo21mSx4M08VTdZ06pxqN2NAmlf23jJZJWRy8mLHi%2BIl%2FvvTCmkeO9VM9S1SHGKf%2F3iZS7IlQMvGHyE7XBf1SEv4R3v7aungv6rMQNClv6DRjXqSwjEuoo43CCUi3SHbwZXQOylXhreHWG%2BqHEbPt5IRvUQSW985LaJvq0%2BBOYVlN%2FeF6QUKCJVFKNhNaKj9e3hp2j6oxbNyQamvnTBH3O9Efd9lzRL3Zp7Bk9vzNIf4sWUa07mvsGfk0i3%2BdPj76O5APt3EotVb3wK9RfRab6wirQ6xSVib%2BqfYrFvejWyxwkvPRSvf4Dkq3Qdv6ie90dZ9xstrte4UvQ50HT4d3jYQZ3n0wUjuH2YGfzSiD7xZGhT9P4QKikb7YTVAuB6SCHRUAa%2BEgCskhyuPfyqk41brjzJPoUf2Gn30xTcmNfRuK2yX%2BHPXu%2FSJAqlsl7iGvPfo6EA%3D--7Ir8evTtVlEFwZM2--mujUEDNrlIfgy%2F9jgZI94A%3D%3D; _uetsid=8ebca870371f11ed884985c548b089b3; _uetvid=da25dc7032bb11edbbfde3a1a6ee4e33; ab.storage.sessionId.f9062f4a-69b2-4d6b-a39c-23bc77cf4004=%7B%22g%22%3A%2209d0158c-ff14-6d1c-9ce3-90d47111e825%22%2C%22e%22%3A1663486950373%2C%22c%22%3A1663484520588%2C%22l%22%3A1663485150373%7D; _ga=GA1.2.191145449.1663001792",
        "authority": "api.sorare.com",
        "accept": "application/json",
        "accept-language": "en-US",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://sorare.com",

    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data=json.loads(response.text)
    slug=data['data']['competition']['country']['slug']

    country=pycountry.countries.get(alpha_2=f'{slug}')
    return country.name
