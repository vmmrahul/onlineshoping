d= [{'id': '3', 'name': 'Solimo Vegetable Chopper', 'price': '256', 'image': '/media/productImages/download.webp', 'qty': 1, 'totalPrice': 256.0}, {'id': '4', 'name': 'olimo Stainless Steel Induction Bottom Steamer', 'price': '799', 'image': '/media/productImages/81ry%2BZ3KACL._SL1500_.jpg', 'qty': 1, 'totalPrice': 799.0}]
#
for item in d:
    if item['qty']==1 and item['id']=='3':
        del d[1]


print()
