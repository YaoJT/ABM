import arcpy
import images2gif
from PIL import Image,ImageDraw,ImageFont
import os
import matplotlib.pyplot as plt
import numpy as np

def create_gif(images,title_list,xy,font,color,out_file,duration = 0.2,resize = 1):
    ## Image Open
    iml = [Image.open(im) for im in images]
    imll = []                         
##    iml = [x.resize((int(x.size[0]*resize),int(x.size[1]*resize))) for x in iml]
    for i in range(len(iml)):
        draw = ImageDraw.Draw(iml[i])
        draw.text((xy[0],xy[1]),title_list[i],color,font=font)
    for im in iml:
        im.thumbnail((int(im.size[0]*resize),int(im.size[1]*resize)))
        imll.append(im)
    images2gif.writeGif(out_file,imll,duration)
    return out_file
def create_dd_graph(data,x,x_range,y_range,x_label,y_label,out_file,color_list):
    plt.axis(x_range+y_range)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    bottom = 0
    for i in range(len(data)):
        top = bottom + data[i]
        plt.plot(top,'-*',color=(0,0,0))
        plt.fill_between(x,bottom,top,color=color_list[i])
        bottom = top
    plt.savefig(out_file)
    return out_file
def get_radio(in_raster):
    out_res = {}
    array = arcpy.RasterToNumPyArray(in_raster)
    none_value = arcpy.Raster(in_raster).noDataValue
    value_list = list(np.unique(array))
    value_list.remove(none_value)
    total = 0.0
    for value in value_list:
        out_res[value]=np.sum(array==value)
        total += out_res[value]
    for value in value_list:
        out_res[value] = out_res[value]/total*100
    return out_res
        
    
    

if __name__ == '__main__':
    arcpy.CheckOutExtension('spatial')
    arcpy.env.overwriteOutput = True
    work_space = 'd:/Github/ABM/images_web'
    if os.path.exists(work_space) == False:
        os.makedirs(work_space)
### create images of simulating
    mxd = 'g:/AgentBasedModel/2015Final/model_web1.mxd'
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
        arcpy.mapping.ExportToJPEG(mxd_map,im_path,resolution = 72)
        images.append(im_path)
        print im_path
### create gif
    xy = (920,250)
    color = 1
    font = ImageFont.truetype("c:/windows/Fonts/times.ttf",30)
    out_file = os.path.join(work_space,'change12_18.gif')
    create_gif(images,year_list,xy,font,color,out_file,duration = 0.5,resize = 1)
    os.system(out_file)    

### create images of validating
## create focal maps
##    validate_list = ['G:/AgentBasedModel/2015Final/result/11-812/compare_'+str(i) for i in range(11)]    
##    observe_2012 = 'g:/AgentBasedModel/validating_100/2012'
##    observe_2015 = 'g:/AgentBasedModel/validating_100/2015'
##    simulate_2015 = 'g:/AgentBasedModel/validating_100/predict'
##    out_space = 'g:/AgentBasedModel/2015Final/validaing_1216ff/'
##    if os.path.exists(out_space) == False:
##        os.makedirs(out_space)
##    radio_list = [str(x)+'00 m' for x in range(len(validate_list))]
####    ob_2012_list = [out_space+'observe2012_'+str(i)+'.tif' for i in range(len(validate_list))]
####    ob_2015_list = [out_space+'observe2015_'+str(i)+'.tif' for i in range(len(validate_list))]
####    sm_2015_list = [out_space+'simulate2015_'+str(i)+'.tif' for i in range(len(validate_list))]
##    ob_2012_list,ob_2015_list,sm_2015_list = [],[],[]
##    for i in range(len(validate_list)):
##        arcpy.env.mask = observe_2012
##        ob_2012_path = out_space+'ob2012_'+str(i)
##        ob_2015_path = out_space+'ob2015_'+str(i)
##        sm_2015_path = out_space+'sm2015_'+str(i)
##        if i != 0:            
##            if os.path.exists(ob_2012_path) == False:
##                ob_2012 = arcpy.sa.FocalStatistics(observe_2012,arcpy.sa.NbrCircle(i,'CELL'),'MAJORITY')
##                ob_2012.save(ob_2012_path)
##            print ob_2012_path
##            ob_2012_list.append(ob_2012_path)
##            if os.path.exists(ob_2015_path) == False:
##                ob_2015 = arcpy.sa.FocalStatistics(observe_2015,arcpy.sa.NbrCircle(i,'CELL'),'MAJORITY')
##                ob_2015.save(ob_2015_path)
##            print ob_2015_path
##            ob_2015_list.append(ob_2015_path)            
##            if os.path.exists(sm_2015_path) == False:
##                sm_2015 = arcpy.sa.FocalStatistics(simulate_2015,arcpy.sa.NbrCircle(i,'CELL'),'MAJORITY')
##                sm_2015.save(sm_2015_path)
##            print sm_2015_path
##            sm_2015_list.append(sm_2015_path)
##        else:
##            if os.path.exists(ob_2012_path) == False:
##                ob_2012 = arcpy.Raster(observe_2012)
##                ob_2012.save(ob_2012_path)
##            print ob_2012_path
##            ob_2012_list.append(ob_2012_path)
##            if os.path.exists(ob_2015_path) == False:
##                ob_2015 = arcpy.Raster(observe_2015)
##                ob_2012.save(ob_2015_path)
##            print ob_2015_path
##            ob_2015_list.append(ob_2015_path)
##            if os.path.exists(sm_2015_path) == False:
##                sm_2015 = arcpy.Raster(simulate_2015)
##                sm_2015.save(sm_2015_path)
##            print sm_2015_path
##            sm_2015_list.append(sm_2015_path)            
#### create and modify images
##    images = []
##    mxd = 'g:/AgentBasedModel/2015Final/validate12_16_1.mxd'
##    data = [[],[],[],[],[]]
##    for i in range(len(validate_list)):
#### create statistical graph
##        res = get_radio(validate_list[i])
##        for value in res:
##            data[value-1].append(res[value])
##        out_file = os.path.join(work_space,'statistic_%s.png' %i)
##        sta = Image.open(create_dd_graph(np.array(data),range(i+1),[0,10],[91,100],'Fuzzy Radius (*100 m)','ratio %',
##                                         out_file,[(190/255.0,232/255.0,255/255.0),(119/255.0,20/255.0,235/255.0),
##                                                   (36/255.0,205/255.0,2/255.0),(250/255.0,41/255.0,34/255.0),
##                                                   (255/255.0,235/255.0,176/255.0)]))
##        print out_file       
#### create map graph
##        map_mxd = arcpy.mapping.MapDocument(mxd)
##        out_file = os.path.join(work_space,'validating_%s.jpg' %i)
#### replace datasource
##        for lyr in arcpy.mapping.ListLayers(map_mxd):
##            if lyr.name == 'observe_2012':
##                lyr.replaceDataSource(out_space,"RASTER_WORKSPACE",'ob2012_'+str(i))
##                print 'ob2012_'+str(i)
##            elif lyr.name == 'observe_2015':
##                lyr.replaceDataSource(out_space,"RASTER_WORKSPACE",'ob2015_'+str(i))
##                print 'ob2015_'+str(i)
##            elif lyr.name == 'simulate_2015':
##                lyr.replaceDataSource(out_space,"RASTER_WORKSPACE",'sm2015_'+str(i))
##                print 'sm2015_'+str(i)
##            elif lyr.name == 'validate':
##                lyr.replaceDataSource('G:/AgentBasedModel/2015Final/result/11-812',"RASTER_WORKSPACE",'compare_'+str(i))
##                print 'compare_'+str(i)           
##        arcpy.mapping.ExportToJPEG(map_mxd,out_file)
##        print out_file
##        del map_mxd
##        im = Image.open(out_file)
##        sta.thumbnail((int(400*1.35),int(300*1.35)))
##        im.paste(sta,(1150,0))
##        im.save(os.path.join(work_space,'validating&sta_%s.jpg' %i))
##        images.append(os.path.join(work_space,'validating&sta_%s.jpg' %i))
##    arcpy.CheckInExtension('spatil')
        
### create gif
##    images1 = ['D:/Github/ABM/images/validating&sta_x.jpg'.replace('_x','_'+str(x)) for x in range(10)]
##    resize1 = 384.0/1686*2.5
##    images2 = ['D:/Github/ABM/images/year_x.jpg'.replace('_x','_'+str(x)) for x in range(2012,2021)]
##    resize2 = 384.0/1123*2.5
##    xy1 = (640,130)
##    xy2 = (917,246)
##    color = 1
##    font1 = ImageFont.truetype("c:/windows/Fonts/ARLRDBD.TTF",50)
##    font2 = ImageFont.truetype("c:/windows/Fonts/times.ttf",30)
##    out_file1 = os.path.join(work_space,'validate_mid.gif')
##    out_file2 = os.path.join(work_space,'simulate_mid.gif')
##    create_gif(images1,[str(x)+'00 m' for x in range(11)],xy1,font1,color,out_file1,duration = 0.5,resize = resize1)
##    os.system(out_file1)
##    create_gif(images2,['year_'+str(x) for x in range(2012,2021)],xy2,font2,color,out_file2,duration = 0.5,resize = resize2)
##    os.system(out_file2)   
        
