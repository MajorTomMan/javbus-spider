import  requests


response=requests.get('https://www.cdnbus.shop/ajax/uncledatoolsbyajax.php?gid=11225907343&lang=zh&img=/imgs/cover/1tx1_b.jpg&uc=1&floor=863')
print(response.status_code)
print(response.content)