# text_classifier
유저가 작성한 제목/내용을 활용하여 적절한 카테고리로 분류하는 문제로, 카테고리는 대분류/중분류/소분류의 계층으로 구성되어있다. 본 repository는 해당문제를 풀기위한 base line으로 실제 적용된 모델과는 차이가 있다. 

## model
01. hierarchical model
하위 카테고리 분류시, 상위 카테고리의 결과를 이용한다면 분류가 용이할 것이라는 컨셉으로 만든 모델로 multi-channel로 대분류와 중분류를 분류하고, 그 결과를 소분류 분류기에 input으로 사용하는 모델이다. 대분류 분류부터 소분류 분류까지 end-to-end모델로 각 분류별 loss의 weight를 사용자가 설정할 수 있다.  

## input data 
input data는 json파일로, 아래와 같은 형태로 구성된다.

id            : key column으로 12자리 숫자이다, string
cateCode      : 대/중/소분류 코드로 각각 계층별 분류코드는 영문철자1자리고 구성된다. string
(ex. cateCode가 ABC -> 대분류 A, 중분류 B, 소분류 C를 의미한다)
title         : 문의 제목, string
cont          : 문의 내용, string
product_name  : 문의한 상품명, string

| id           | cateCode | title | cont      | product_name |
|--------------|----------|-------|-----------|--------------|
| 201808010001 | AAB      | abc.. | abcde.... | abcdef....   |
| ............ | ...      | ...   | .....     | .....        |
