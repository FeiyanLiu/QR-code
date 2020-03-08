import cv2
img=cv2.imread('/Users/xianfu/Downloads/test3.JPG')
#img=reshape_image(img)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
contours,hierachy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#获取轮廓
m=[]
n=[]
j=0
for i in range(len(contours)):
        child = hierachy[0][i][2]

        if child!=-1:
            child_child=hierachy[0][child][2]
            if child_child!=-1:
                #if cv2.contourArea(contours[child])/cv2.contourArea(contours[child_child])>=1 and cv2.contourArea(contours[child])/cv2.contourArea(contours[child_child])<=2 :
                 #   print(i)
                m.append(contours[i])
                n.append(i)

cv2.drawContours(img, m, -1, (0, 0, 255), 2)#提取轮廓
cv2.imwrite(r'/Users/xianfu/Downloads/23.jpg',img)
#print(m)
#print(n)
#cnt = np.array(m[0],m[1],m[2])#变成二维数组
m1=np.asarray(m[0]).reshape((-1,2))
m2=np.asarray(m[1]).reshape((-1,2))
m3=np.asarray(m[2]).reshape((-1,2))
ts = np.concatenate((m1,m2,m3))
rect = cv2.minAreaRect(ts) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
#print(box)
box = np.int0(box)#取整数
#print(box)
# 画出来
leftup=box[2][1]
rightup=box[0][1]
leftbottom=box[1][0]
rightbottom=box[3][0]
new_img= img[leftup:rightup,leftbottom:rightbottom]
new_img=cv2.resize(new_img,(512,512))
cv2.imwrite(r'/Users/xianfu/Downloads/24.jpg',new_img)
