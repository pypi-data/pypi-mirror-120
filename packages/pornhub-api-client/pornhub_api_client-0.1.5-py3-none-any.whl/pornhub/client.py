from typing import List
import json
import requests
import logging
from pornhub.response_codes import check_response

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class PornhubApi:
    """This class creates functions that interact with pornhub.com

    Returns:
        functions: returns different api functions that interact with pornhub
    """

    URL = "https://www.pornhub.com/webmasters"

    def make_url(self, path: str) -> str:
        """Concate base url with string from specific method"""
        return f"{self.URL}{path}"

    def make_request(self, url: str, params=None) -> json:
        """this function makes api request to pornhub

        Args:
            url (String): unique url for each method
            params (List, optional): search parameters. Defaults to None.

        Returns:
            json: returns json answer from pronhub
        """

        try:
            response = requests.get(url, params=params)
            response = response.json()
            check_response(response)

        except requests.exceptions.ConnectionError as error:
            logging.warning(f"{error}")
            return None
        except ValueError as val_error:
            logging.warning(f"{val_error}")
            return None

        return response

    def search(
        self, query: str = "", thumbsize: str = "small", page: int = 1, **kwargs
    ) -> list:
        """Start searching with parameters

        Args:
            query (str, optional): Search query. Defaults to ''.
            thumbsize (str, optional): Possible values are small, medium, large, small_hd, medium_hd, large_hd. Defaults to 'small'.
            category ([type], optional): Video category. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            ordering ([type], optional): Possible values are featured, newest, mostviewed and rating. Defaults to None.
            phrase (List[str], optional): Used as pornstars filter. Defaults to None.
            tags (List[str], optional): Video tags. Defaults to None.
            period ([type], optional): Works with ordering. Possible values are weekly, monthly, and alltime. Defaults to None.

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.search(query='straight')
            # result ->>
                    {
                    "duration": "11:50",
                    "views": 587,
                    "video_id": "ph5fa1aad36d297",
                    "rating": "100",
                    "ratings": 2,
                    "title": "Fill my mouth with your cum ",
                    "url": "https://www.pornhub.com/view_video.php?viewkey=ph5fa1aad36d297",
                    "default_thumb": "https://di.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)12.jpg",
                    "thumb": "https://di.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)7.jpg",
                    "publish_date": "2021-03-15 18:07:03",
                    "thumbs": [
                        {
                        "size": "320x240",
                        "width": "320",
                        "height": "240",
                        "src": "https://di.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)1.jpg"
                        },
                        {
                        "size": "320x240",
                        "width": "320",
                        "height": "240",
                        "src": "https://di.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)2.jpg"
                        }
                    ],
                    "tags": [
                        {
                        "tag_name": "cum swallow"
                        },
                        {
                        "tag_name": "swallow"
                        }
                    ],
                    "pornstars": [],
                    "categories": [
                        {
                        "category": "amateur"
                        },
                        {
                        "category": "big-tits"
                        }
                    ],
                    "segment": "straight"
                    }
        """

        url = self.make_url("/search")
        params = {"search": query, "page": page, "thumbsize": thumbsize}
        list_params = ["tags", "phrase"]

        for arg, value in kwargs.items():
            if arg in list_params:
                params[f"{arg}[]"] = ",".join(value)
            else:
                params[f"{arg}"] = value

        data = self.make_request(url, params)

        if data:
            return data["videos"]
        return None

    def stars(self) -> list:
        """Get short pornstars list

        Returns:
            json: returns json as searching result with parameters

        Example:
            #
            phb_api = phb.PornhubApi()
            result = phb_api.stars()
            # result ->>
                {
                    "star": {
                        "star_name": "033120 mpp2"
                    }
                    },
                    {
                    "star": {
                        "star_name": "050221mpp"
                    }
                    },
                    {
                    "star": {
                        "star_name": "051220 mpp"
                    }
                    },
                    {
                    "star": {
                        "star_name": "070820mpp"
                    }
                    },
                    {
                    "star": {
                        "star_name": "070920mpp"
                    }
                    },
                    {
                    "star": {
                        "star_name": "2 Pretty 4 Porn"
                    }
                    },
                    {
                    "star": {
                        "star_name": "29EXP"
                    }
                }

        """

        url = self.make_url("/stars")
        data = self.make_request(url)

        if data:
            return data["stars"]
        return None

    def stars_detailed(self) -> list:
        """Get detailed pornstars list

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.stars_detailed()
            # result ->>
                {
                    "star": {
                        "star_name": " Melisa Wide",
                        "star_thumb": "https://di.phncdn.com/pics/pornstars/default/(m=lciuhScOb_c)(mh=MIYb3JZmqOmG07hE)female.jpg",
                        "star_url": "https://www.pornhub.com/pornstar/videos_overview?pornstar=melisa-wide",
                        "gender": "female",
                        "videos_count_all": "0"
                    }
                    },
                    {
                    "star": {
                        "star_name": ", Arietta Adams",
                        "star_thumb": "https://di.phncdn.com/pics/pornstars/default/(m=lciuhScOb_c)(mh=MIYb3JZmqOmG07hE)female.jpg",
                        "star_url": "https://www.pornhub.com/pornstar/videos_overview?pornstar=%2C-arietta-adams",
                        "gender": "female",
                        "videos_count_all": "0"
                    }
                    },
                    {
                    "star": {
                        "star_name": "033120 mpp2",
                        "star_thumb": "https://di.phncdn.com/pics/pornstars/default/(m=lciuhScOb_c)(mh=MIYb3JZmqOmG07hE)female.jpg",
                        "star_url": "https://www.pornhub.com/pornstar/videos_overview?pornstar=033120-mpp2-changed",
                        "gender": "female",
                        "videos_count_all": "1"
                    }
                    },
                    {
                    "star": {
                        "star_name": "050221mpp",
                        "star_thumb": "https://di.phncdn.com/pics/pornstars/default/(m=lciuhScOb_c)(mh=0gAw-L65LP18RaWB)male.jpg",
                        "star_url": "https://www.pornhub.com/pornstar/videos_overview?pornstar=050221mpp",
                        "gender": "male",
                        "videos_count_all": "0"
                    }
                }

        """

        url = self.make_url("/stars_detailed")
        data = self.make_request(url)

        if data:
            return data["stars"]
        return None

    def video_by_id(self, id: int) -> dict:
        """Get video id

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.video_by_id('ph5fa1aad36d297')
            # result ->>
                {
                    "duration": "11:50",
                    "views": 71,
                    "video_id": "ph5fa1aad36d297",
                    "rating": "100",
                    "ratings": 5,
                    "title": "Fill my mouth with your cum ",
                    "url": "https://www.pornhub.com/view_video.php?viewkey=ph5fa1aad36d297",
                    "default_thumb": "https://ei.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)12.jpg",
                    "thumb": "https://ei.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)7.jpg",
                    "publish_date": "2021-03-15 18:07:03",
                    "thumbs": [
                    {
                        "size": "320x240",
                        "width": "320",
                        "height": "240",
                        "src": "https://ei.phncdn.com/videos/202011/03/366620472/original/(m=eaf8Ggaaaa)(mh=rFCACw3dUGSHJSbA)1.jpg"
                    }
                    ],
                    "tags": [
                    {
                        "tag_name": "cum swallow"
                    },
                    {
                        "tag_name": "swallow"
                    }
                    ],
                    "pornstars": [],
                    "categories": [
                    {
                        "category": "amateur"
                    },
                    {
                        "category": "big-tits"
                    }
                    ],
                    "segment": "straight"
                }
        """

        url = self.make_url("/video_by_id?id=")
        params = {"id": id}
        data = self.make_request(url, params)

        if data:
            return data["video"]
        return None

    def is_video_active(self, id: int) -> dict:
        """Check if video is active

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.is_video_active('ph5fa1aad36d297')
            # result ->>
                {
                    "video_id": "ph5fa1aad36d297",
                    "is_active": "1"
                }
        """

        url = self.make_url("/is_video_active?id=")
        params = {"id": id}
        data = self.make_request(url, params)

        if data:
            return data["active"]
        return None

    def categories(self) -> list:
        """Get all possible categories

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.categories()
            # result ->>
                {
                    "id": "622",
                    "category": "180-1"
                    },
                    {
                    "id": "632",
                    "category": "2d"
                    },
                    {
                    "id": "612",
                    "category": "360-1"
                    },
                    {
                    "id": "642",
                    "category": "3d"
                    },
                    {
                    "id": "105",
                    "category": "60fps-1"
                    },
                    {
                    "id": "252",
                    "category": "amateur-gay"
                    },
                    {
                    "id": "3",
                    "category": "amateur"
                    },
                    {
                    "id": "35",
                    "category": "anal"
                    }
        """

        url = self.make_url("/categories")
        data = self.make_request(url)

        if data:
            return data["categories"]
        return None

    def tags(self, tags: List[str] = None) -> list:
        """Get all tags

        Returns:
            json: returns json as searching result with parameters

        Example:
            phb_api = phb.PornhubApi()
            result = phb_api.tags(a)
            # result ->>
            {
                "warning": "We had to change the response structure due to high amount of tags. Please adjust your code",
                "tagsCount": 322429,
                "tags": [
                    "a",
                    "a 03 26",
                    "a 04 01",
                    "a 04 02",
                    "a 04 03",
                    "a 04 05",
                    "a 04 07",
                    "a 1",
                    "a 1 2",
                    "a 1 2 3",
                    "a 1 amateur",
                    "a 1 asmr",
                    "a 1 blow job",
                    "a 1 cocksukker 1",
                    "a 1 cute",
                    "a 1 fat wood",
                    "a 1 head game",
                    "a 1 pictures",
                    "a 1 pussy",
                    "a 10",
                    "a 10 hr wank",
                    "a 10 warthog",
                    "a 100 bet to the",
                    "a 1000 miles",
                    "a 11",
                    "a 1111",
                    "a 12 pack of beer",
                    "a 123",
                    "a 1253c3c",
                    "a 13 yrs old",
                    "a 13 yry old",
                    "a 18",
                    "a 18 a",
                    "a 18 anal"
                    }
        """

        url = self.make_url("/tags")
        params = None
        if tags is not None:
            params["tags[]"] = ",".join(tags)
        data = self.make_request(url, params)

        if data:
            return data["tags"]
        return None
