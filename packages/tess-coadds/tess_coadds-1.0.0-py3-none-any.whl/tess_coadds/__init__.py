import os
import requests
import urllib.parse
import re

from astropy.io import ascii


class TESSCoadds:

    """

    TESSCoadds class

    The TESS mission is systematically observing a set of wide fields in a regular
    pattern, eventually covering most of the sky except for the ecliptic plane.
    For each field, a set of around 1200 exposures are made and analyzed for time
    variability (specifically looking for planetary transits).

    We have used these same images to create a set of codded plates (336 in total
    so far).  These plates give the best available view of the time-averaged TESS 
    sky.

    This service allows the user to cut sections from the coadds based on location.
    Since the TESS observations overlap, particularly near the ecliptic poles, 
    some locations will have multiple cutouts.  Therefore the processing involves
    two steps:  1) Search the image metadata and identify a list of images covering
    a location and  2) produce a cutout for one of the images.  There is also
    a utility routine that will produce all the cutouts in a single step.

    """


    def __init__(self, location, radius=0.001, server=None, debug=False):

        """

        TESSCoadds() initialization defines the region of interest.  

        Parameters
        ----------
        location : string, required.
            The location can be given as coordinates (e.g. '3h23m15.4s -12d18m34.1s Equ J2000',
            '234.43 -16.91 Gal', etc.) or as an object name (e.g. 'M51', 'Kepler 22'.  Both
            forms a very forgiving concerning syntax.
        radius : float, optional, default=0.001. 
            The service supports inputting a radius in degrees to allow searching for extended 
            objects (i.e. that may span multiple images).
        debug : boolean, optional.
            If True, various bits operating information will be printed out.

        """

        self.server = 'http://exofop.ipac.caltech.edu/cgi-bin/TESSCoadds'

        if server != None:
            self.server = server

        self.locstr = urllib.parse.quote(location)
        self.rad = float(radius)

        if self.rad == None or self.rad <= 0.001:
           self.rad = 0.001

        self.tbldata = []

        self.debug = False

        if debug == True:
            self.debug = debug
            print('DEBUG> Debugging output turned on.')

        self.imglist()

        if debug == True:
            self.debug = debug
            print('DEBUG> Debugging output turned on.')


    def imglist(self):

        """

        imglist() searches the image metadata for the images covering this location.
        The data gets saved locally to a file whose name is based on the search region
        and returned as an Astropy table.

        In addition to the image file names, the table contains the image WCS and the
        four corners of the images as (RA,Dec).

        """

        url = self.server + '/nph-tesslist?locstr=' + self.locstr
        url = url + '&radius=' + str(self.rad)

        if self.debug == True:
            print('DEBUG> URL: ' + str(url))

        tesslist = requests.get(url)

        status_code = tesslist.status_code

        if self.debug == True:
            print('DEBUG> HTTP status code: ' + str(status_code))

        if status_code != 200:
            raise Exception('Image list URL (' + url + ') failed (return code ' + str(status_code) + ')')

        try:
            disposition = tesslist.headers['Content-Disposition']

            filename = re.findall("filename=(.+)", disposition)[0]

        except:
            pass

        if self.debug == True:
            print('DEBUG> File name:        ' + str(filename))

        open(filename, 'wb').write(tesslist.content)

        self.tbldata = ascii.read(filename)

        return self.tbldata



    def cutout(self, tessfile, boxsize):

        """

        cutout() returns a FITS file cutout from the named image (from image metadata list).
        
        Parameters
        ----------
        tessfile : string, required.
            A TESS coadd file name (from the metadata list '3h23m15.4s -12d18m34.1s Equ J2000',
            '234.43 -16.91 Gal', etc.) or as an object name (e.g. 'M51', 'Kepler 22'.  Both
            forms a very forgiving concerning syntax.
        radius : float, optional, default=0.001. 
            The service supports inputting a radius in degrees to allow searching for extended 
            objects (i.e. that may span multiple images).

        """

        if len(self.tbldata) == 0:
            self.imglist()

        url = self.server + '/nph-tesscutout?locstr=' + str(self.locstr) + '&size=' + str(boxsize) + '&file=' + tessfile

        if self.debug == True:
            print('DEBUG> URL: ' + str(url))

        tesscutout = requests.get(url)

        status_code = tesscutout.status_code

        if self.debug == True:
            print('DEBUG> HTTP status code: ' + str(status_code))

        if status_code != 200:
            raise Exception('Image cutout URL (' + url + ') failed (return code ' + str(status_code) + ')')

        disposition = tesscutout.headers['Content-Disposition']

        cutout_filename = re.findall("filename=(.+)", disposition)[0]

        if self.debug == True:
            print('DEBUG> File name:        ' + str(cutout_filename))

        open(cutout_filename, 'wb').write(tesscutout.content)

        return cutout_filename



    def cutouts(self, boxsize):

        """

        cutout() returns a FITS file cutout from the named image (from image metadata list).
        
        Parameters
        ----------
        tessfile : string, required.
            A TESS coadd file name (from the metadata list '3h23m15.4s -12d18m34.1s Equ J2000',
            '234.43 -16.91 Gal', etc.) or as an object name (e.g. 'M51', 'Kepler 22'.  Both
            forms a very forgiving concerning syntax.
        radius : float, optional, default=0.001. 
            The service supports inputting a radius in degrees to allow searching for extended 
            objects (i.e. that may span multiple images).

        """

        cutout_filenames = []

        if len(self.tbldata) == 0:
            self.imglist()

        filenames = self.tbldata['fname']

        for filename in filenames:
            cutout_filename = self.cutout(filename, boxsize)
            cutout_filenames.append(cutout_filename)

        return cutout_filenames
