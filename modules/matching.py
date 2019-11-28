import numpy as np
import matplotlib.pyplot as plt
import cv2

def match(img,template):
    """ Compute correlation of template over img using NCC metric with stride 1.

    """
    r0, c0,_ = img.shape
    r1, c1,_ = template.shape
    rs = np.zeros((r0-r1+1,c0-c1+1))
    mt = np.mean(template, axis=(0,1)) # mean of template
    std_t = np.std(template, axis=(0,1))
    for i in range(r0-r1+1):
        for j in range(c0-c1+1):
            mx = np.mean(img[i:i+r1,j:j+c1,:], axis=(0,1))  # mean of image
            std_x = np.std(img[i:i+r1,j:j+c1,:], axis=(0,1))
            rs[i,j] = np.sum( (img[i:i+r1,j:j+c1,:] - mx[np.newaxis,np.newaxis,...]) *(template - mt[np.newaxis,np.newaxis,...]) / (std_x*std_t)) / (r1*c1-1) # divide ncc by unbiased count


    return rs


if __name__=="__main__":
    # img = cv2.imread('../out/000040.png')
   
    # template = cv2.imread('../out/template.png')
    
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
    img = cv2.imread('../out/search.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    template = cv2.imread('../out/template1.png')
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    print(img.shape)
    # img = img[::4,::4,:]
    # template = template[::4,::4,:]
    result = match(img,template)





    candidates = np.argsort(result, axis=None)
    k_match = candidates[-1] # k top result
    # print(k_match.shape)
    r1, c1,_ = template.shape
    k_match = np.unravel_index(k_match, (img.shape[0]-r1+1,img.shape[1]-c1+1))
    print(k_match)
    #ax = figs.add_subplot(1,len(K)+1,k+2)
    #ax.title.set_text('k={}'.format(K[k]))
    plt.imshow(img[k_match[0]:k_match[0]+r1,k_match[1]:k_match[1]+c1,:])
    plt.show()
