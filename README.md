:bookmark: 전체 영화 목록 조회

[GET]http://127.0.0.1:8000/movies/

```json
[
    {
        "id": 1,
        "title": "고질라 VS. 콩",
        "overview": "콩과 보호자들은 정착할 수 있는 곳을 찾아 특별하고 강력한 유대감을 형성하고 있는 지아와 함께 여정을 떠나게 된다. 그러던 중 지구 파괴를 위한 회심의 날을 휘두르는 고질라와 마주하게 되고, 보이지 않는 힘에 의해 맞붙게 된 두 전설의 대결은 지구 깊은 곳에 도사린 수수께끼의 시작에 불과할 뿐이었는데…",
        "release_date": "2021-03-24",
        "poster_path": "https://www.themoviedb.org/t/p/original/sqo672rKMXiLRC5kVcGvBRebkp.jpg"
    },
    {
        "id": 2,
        "title": "노바디",
        "overview": "비범한 과거를 숨긴 채 남들과 다를 바 없는 평범한 일상을 사는 한 가정의 가장 ‘허치’ 매일 출근을 하고, 분리수거를 하고 일과 가정 모두 나름 최선을 다하지만 아들한테는 무시당하고 아내와의 관계도 소원하다. 그러던 어느 날, 집안에 강도가 들고 허치는 한 번의 반항도 하지 못하고 당한다. 더 큰 위험으로부터 가족을 지키기 위한 선택이었는데 모두 무능력하다고 ‘허치’를 비난하고, 결국 그동안 참고 억눌렀던 분노가 폭발하고 만다.",
        "release_date": "2021-03-26",
        "poster_path": "https://www.themoviedb.org/t/p/original/oXQtH8O7pCvXaDKGB8OAjiPVDi5.jpg"
    },
    {
        "id": 3,
        "title": "극장판 귀멸의 칼날: 무한열차 편",
        "overview": "혈귀로 변해버린 여동생 ‘네즈코’를 인간으로 되돌릴 단서를 찾아 비밀조직 귀살대에 들어간 ‘탄지로.’ ‘젠이츠’, ‘이노스케’와 새로운 임무 수행을 위해 무한열차에 탑승 후 귀살대 최강 검사 염주 ‘렌고쿠’와 합류한다. 달리는 무한열차에서 승객들이 하나 둘 흔적 없이 사라지자 숨어있는 식인 혈귀의 존재를 직감하는 ‘렌고쿠’. 귀살대 ‘탄지로’ 일행과 최강 검사 염주 ‘렌고쿠’는 어둠 속을 달리는 무한열차에서 모두의 목숨을 구하기 위해 예측불가능한 능력을 가진 혈귀와 목숨을 건 혈전을 시작하는데…",
        "release_date": "2020-10-16",
        "poster_path": "https://www.themoviedb.org/t/p/original/tDAQALgC407eg3SVAgehbiMwqo0.jpg"
    },
    //중략
]
```



:bookmark: 단일 영화 정보 조회

[GET]http://127.0.0.1:8000/movies/movie_pk/

```json
{
    "id": 1,
    "reviews": [
        {
            "id": 1,
            "content": "굿",
            "rank": 10,
            "created_at": "2021-05-22T21:09:30.754684Z",
            "movie": 1,
            "create_user": 1,
            "like_users": [],
            "dislike_users": []
        }
    ],
    "title": "고질라 VS. 콩",
    "overview": "콩과 보호자들은 정착할 수 있는 곳을 찾아 특별하고 강력한 유대감을 형성하고 있는 지아와 함께 여정을 떠나게 된다. 그러던 중 지구 파괴를 위한 회심의 날을 휘두르는 고질라와 마주하게 되고, 보이지 않는 힘에 의해 맞붙게 된 두 전설의 대결은 지구 깊은 곳에 도사린 수수께끼의 시작에 불과할 뿐이었는데…",
    "release_date": "2021-03-24",
    "poster_path": "https://www.themoviedb.org/t/p/original/sqo672rKMXiLRC5kVcGvBRebkp.jpg"
}
```



:bookmark: 단일 영화 리뷰 목록 조회

[GET]http://127.0.0.1:8000/movies/movie_pk/reviews/

```json
[
    {
        "id": 1,
        "content": "굿",
        "rank": 10,
        "created_at": "2021-05-22T21:09:30.754684Z",
        "movie": 1,
        "create_user": 1,
        "like_users": [],
        "dislike_users": []
    }
]
```



:bookmark: 리뷰 추가

[POST]http://127.0.0.1:8000/movies/movie_pk/reviews/

```json
{
    "id": 2,
    "content": "최",
    "rank": 10,
    "created_at": "2021-05-22T21:13:19.349284Z",
    "movie": 2,
    "create_user": 1,
    "like_users": [],
    "dislike_users": []
}
```

:white_check_mark: 구현을 위해 작성한 user는 pk값이 1인 유저로 추가되게 함. 향후 수정 필요



:bookmark:리뷰 삭제

[DELETE]http://127.0.0.1:8000/movies/reviews/review_pk/

```json
{
    "success": true,
    "message": "2번 리뷰 삭제"
}
```



:bookmark:리뷰 상세 조회

[GET]http://127.0.0.1:8000/movies/reviews/review_pk/

```json
{
    "id": 1,
    "comments": [],
    "content": "굿",
    "rank": 10,
    "created_at": "2021-05-22T21:09:30.754684Z",
    "movie": 1,
    "create_user": 1,
    "like_users": [],
    "dislike_users": []
}
```



:bookmark: 리뷰 수정

[PUT]http://127.0.0.1:8000/movies/reviews/review_pk/

```json
{
    "id": 1,
    "comments": [],
    "content": "너무 좋아",
    "rank": 10,
    "created_at": "2021-05-22T21:09:30.754684Z",
    "movie": 1,
    "create_user": 1,
    "like_users": [],
    "dislike_users": []
}
```

