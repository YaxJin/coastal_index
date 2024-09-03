# coastal_index

# Introduction
- **【今年夏天一起去看海，一起 AI (愛)上淨灘！】**
    - 為了響應於每年9月第三個週六舉辦的**國際淨灘日**活動(International Coastal Cleanup, ICC)，我們希望以**AI (愛)上淨灘平台，** 提升人們參與淨灘活動之意願，讓大家互相分享淨灘成果、督促彼此，期許能共同打造地球上乾淨美麗的海洋環境!
    - 上傳你附近的海灘照片，讓精準的海岸污染AI辨識系統為你評分！
    - 「淨」情上傳你的淨灘成果，為家鄉的海獲得更高的評分與排名！
    - 誰說AI技術不近人情? 讓我們一起用AI(愛)守護台灣的美麗海岸！
    - 對著目標圖片點擊三下，來找找我們藏好的小彩蛋吧!

# Installation
## docker
**build img:**
```python=
docker build -t tag-name .
```

**run container:**
```python=
docker run -p 8080:8080 tag-name
```

## run flask 
```python=
python router.py
```
# Features
- **AI (愛)上淨灘**是一個即時AI辨識海岸污染的互動網頁平台，其特色包含:
    - 以精準的AI辨識模型偵測海灘圖片中有多少海岸廢棄物，給予其汙染指數並針對各個地區總汙染程度進行排名。
    - 互動網頁中的即時AI辨識功能及動態汙染排名，刺激人們參與和舉辦淨灘活動並上傳他們的淨灘成果，為自己身邊的海岸盡一份心力!
    - 更多淨灘的知識、活動等相關資訊讓淨灘融入生活、不再那麼遙不可及!

# Future 
- more card title 置頂
- 上傳圖片時可選擇拍照時間
- 上傳圖片選擇地點改用GPS座標定位
- 地圖hover時顯示地區名稱

# Contributors
<table>
  <tr>
   <td align="center"><a href="https://github.com/bobho1999"><img src="flask/static/img/Bob_cat.png" width="100px;" alt="bob" width="100px;"/><br /><sub><b>Bob Ho</b></sub></a><br /><a href="https://github.com/YaxJin/coastal_index/commits?author=bobho1999" title="Code">💻</a> <a href="https://github.com/YaxJin/coastal_index/commits?author=bobho1999" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/YaxJin"><img src="flask/static/img/YJ.png" width="100px;" alt="YaJin"/><br /><sub><b>Ya-Jin</b></sub></a><br /><a href="https://github.com/YaxJin/coastal_index/commits?author=YaxJin" title="Code">💻</a> <a href="https://github.com/YaxJin/coastal_index/commits?author=YaxJin" title="UI/UX Design">🎨</a></td>
    <td align="center"><a href="https://github.com/Emmaliu-coder"><img src= "flask/static/img/emma.png" width="100px;" alt="Emma"/><br /><sub><b>Emma Liu</b></sub></a><br /><a href="https://github.com/YaxJin/coastal_index/commits?author=Emmaliu-coder" title="Code">💻</a></td>
  </tr>
</table>

# Resources
[AI (愛)上淨灘](https://learn.pixetto.ai/coastal-index/)

[2022 VIA Summer Internship](https://www.viatech.com/en/careers/internships/)




