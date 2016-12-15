import arcpy
import images2gif
from PIL import Image,ImageDraw,ImageFont
import os

def create_gif(images,title_list,xy,font,color,out_file,duration = 0.2,resize = 1):
    ## Image Open
    iml = [Image.open(im) for im in images]
    iml = [x.resize((int(x.size[0]*resize),int(x.size[1]*resize))) for x in iml]
    for i in range(len(iml)):
        draw = ImageDraw.Draw(iml[i])
        draw.text((xy[0]*resize,xy[1]*resize),title_list[i],color,font=font)
    images2gif.writeGif(out_file,iml,duration)
    return out_file

if __name__ == '__main__':
    work_space = 'd:/Github/ABM/images'
    if os.path.exists(work_space) == False:
        os.makedirs(work_space)
### create images
    mxd = 'g:/AgentBasedModel/2015Final/model_1215f.mxd'
    feature = 'G:/AgentBasedModel/2015Final/landowner.shp'
    year_list = ['year_'+str(x) for x in range(2012,2021)]
    year_fields = ['firstyear']+['year'+str(x) for x in range(1,9)]
    field_name = 'landuse'
    images = []
    for i in range(len(year_list)):
        Row = arcpy.UpdateCursor(feature,[field_name,year_fields[i]])
        for row in Row:
            row.setValue(field_name,row.getValue(year_fields[i]))
            Row.updateRow(row)
        del Row,row
        mxd_map = arcpy.mapping.MapDocument(mxd)
        im_path = os.path.join(work_space,year_list[i]+'.jpg')
        arcpy.mapping.ExportToJPEG(mxd_map,im_path)
        images.append(im_path)
        print im_path
### create gif
    xy = (917,246)
    color = 1
    font = ImageFont.truetype("c:/windows/Fonts/times.ttf",30)
    out_file = os.path.join(work_space,'change12_18.gif')
    create_gif(images,year_list,xy,font,color,out_file,duration = 0.5,resize = 1)
    os.system(out_file)    

        
