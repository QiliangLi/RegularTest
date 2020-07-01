import os
from kindle_maker import make_mobi

def main():
    rootDir=r""
    destDir = r""
    chapterList=os.listdir(rootDir)
    chapter2LectureMapper={}
    sourceList=[]
    for chapter in chapterList:
        chapterPath=os.path.join(rootDir,chapter)
        lectureList=os.listdir(chapterPath)

if __name__=="__main__":
    # main()
    make_mobi(r"E:\24-Java并发编程实战（完结）\03-第一部分：并发理论基础 (13讲)",r"E:\24-Java并发编程实战（完结）\Test")