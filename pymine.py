"""
------------
PyMine 1.0.1
------------
PyMine lets you integrate and visualize biological data used for drug discovery using PyMOL. 

------------
REQUIREMENTS
------------
1) Ubuntu 11.04 or above OR Mac OS X 10.7 or above
2) Pymol 1.7 or above
3) PyMine 1.0.1

------------
INSTALLATION
------------
1) Download and install pymol. http://sourceforge.net/projects/pymol/
2) Download and unzip PyMine. https://github.com/rrchaudhari/PyMine
3) Open PyMol. Install PyMine: Plugins -> Manage Plugins -> Install -> (locate pymine.py file).
4) Restart PyMol

Using MacPyMOL  
1) Rename the "MacPyMOL.app" to "PyMOLX11Hybrid.app" in Applications folder. 
2) install XQuartz found at http://xquartz.macosforge.org/landing/
3) Follow the installatin procedure of plugin mentioned above. 

-----
USAGE
-----
1) Start PyMol and go to Plugins -> PyMine
2) Type the PDB id and chain id of the interested target and click SUBMIT. 
3) To find similar ligands, enter smile string into smile text box (control-v) and click on Find Similar Ligands button.

-------
RESULTS
-------
1) In PyMOL graphics viewer SAPs and Binding Sites data will be available for viewing.
2) In PyMine GUI data will be available and accessed using relevant tabs/buttons.
3) Output files will be saved in a desktop folder named "PyMine_outdir_xxxx". 

-------
History
-------
- v1.0.0: Initial public release

-------------
Licence (MIT)
-------------

Copyright (c) 2015 Rajan Chaudhari and Zhijun Li

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import os
import sys
import fileinput
import Tkinter
import tkMessageBox
import urllib2
import pymol
from Tkinter import PhotoImage as PI
import xml.etree.ElementTree as ET
import webbrowser
import tkFileDialog

#initialize pymol plugin
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command',
                        'Gather information',
                        label = 'PyMine',
                        command = main)
class PyMine(Tkinter.Tk): 
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.grid()
        self.createGUI()
        
        # GLOBAL VARIABLE ARE DEFINED HERE SO THAT THEY CAN BE USED IN ANY FUNCTION
        self.flag=0
        self.pdb_id=''
        self.pdb_chain_id=''
        self.pdb_file=''
        self.smiles=''
        self.name=list()
        self.summary=list()
        self.symbol=list()
        self.uniprot=list()
        self.binding_sites=list()
        self.ppi_bs_residues=''
        self.lig_bs_residues=''
        self.dna_bs_residues=''
        self.rna_bs_residues=''
        self.ion_bs_residues=''
        self.pep_bs_residues=''
        self.ki_comps=list()
        self.ec50_comps=list()
        self.ic50_comps=list()
        self.pathways=list()
        self.saps=list()
        self.ligands=list()
        self.ligand_chemblid=list()
        self.target_chemblID=''
        self.approved_drugs=list()
        self.ligand_images=list()
        self.kegg_info=''
        self.userpdbfile=None
        #self.label4.config(text=None)
        self.entryVariable5.set(None)

    def createGUI(self):
        ## Create Frame
        self.frame1=Tkinter.Frame(self)
        self.frame1.grid(sticky='nswe')

        ## INPUT 
        self.label1=Tkinter.Label(self.frame1, text="Enter PDB ID")   #LABEL
        self.label1.grid(row=1, column=0, sticky=Tkinter.W)
        
        self.entryVariable1=Tkinter.StringVar(master=self.frame1)  #INPUT Variable
        self.entryVariable1.set('1RTK')
        
        self.entry1=Tkinter.Entry(self.frame1, textvariable=self.entryVariable1, width=4) #INPUT Box
        self.entry1.grid(row=1, column=1, sticky=Tkinter.W)

        self.label1_1=Tkinter.Label(self.frame1, text="Enter Chain ID")   #LABEL
        self.label1_1.grid(row=1, column=2, sticky=Tkinter.W)

        self.entryVariable2=Tkinter.StringVar(master=self.frame1) #Input Variable 2 
        self.entryVariable2.set('A')
        
        self.entry2=Tkinter.Entry(self.frame1, textvariable=self.entryVariable2, width=2) #input box 2
        self.entry2.grid(row=1, column=3, sticky=Tkinter.W)
        
        self.label2_2=Tkinter.Label(self.frame1, text="OR")   #LABEL
        self.label2_2.grid(row=1, column=4, sticky=Tkinter.W)

        #self.button1=Tkinter.Button(self.frame1, text="Submit", command=self.get_results) #Button1
        #self.button1.grid(row=1, column=4, sticky=Tkinter.W)
        
        self.button2=Tkinter.Button(self.frame1, text="Clear", command=self.clear) #Button2
        self.button2.grid(row=4, column=4, sticky=Tkinter.W)

        self.label3=Tkinter.Label(self.frame1, text="Select PDB File")   #LABEL
        self.label3.grid(row=2, column=0, sticky=Tkinter.W)

        self.button1_1=Tkinter.Button(self.frame1, text="Browse", command=self.file_upload) #Button2
        self.button1_1.grid(row=2, column=1, sticky=Tkinter.W) 

        self.label5=Tkinter.Label(self.frame1, text="Enter Uniprot ID")   #LABEL
        self.label5.grid(row=2, column=2, sticky=Tkinter.W)

        self.entryVariable5=Tkinter.StringVar(master=self.frame1) #Input Variable 3 
        self.entryVariable5.set('')
        
        self.entry5=Tkinter.Entry(self.frame1, textvariable=self.entryVariable5, width=6) #input box 3
        self.entry5.grid(row=2, column=3, sticky=Tkinter.W)


        self.button2_2=Tkinter.Button(self.frame1, text="Submit", command=self.get_results) #Button1
        self.button2_2.grid(row=2, column=4, sticky=Tkinter.W)

        self.label4=Tkinter.Label(self.frame1, width=10, anchor=Tkinter.W, justify=Tkinter.LEFT)   #LABEL
        self.label4.grid(row=3, column=1, sticky=Tkinter.W) 


        self.label2=Tkinter.Label(self.frame1, text="Enter Smile String")   #LABEL
        self.label2.grid(row=4, column=0, sticky=Tkinter.W)

        self.entryVariable3=Tkinter.StringVar(master=self.frame1) #Input Variable 3 
        self.entryVariable3.set('')
        
        self.entry3=Tkinter.Entry(self.frame1, textvariable=self.entryVariable3, width=10) #input box 3
        self.entry3.grid(row=4, column=1, columnspan=2, sticky=Tkinter.W)
        
        self.button3=Tkinter.Button(self.frame1, text="Find Similar Ligands", command=self.get_similar_ligands) #Button2
        self.button3.grid(row=4, column=2, sticky=Tkinter.W)
        
        self.button11=Tkinter.Button(self.frame1, text="?", command=self.smiles_help)
        self.button11.grid(row=4, column=3, sticky=Tkinter.W)

        ## OUTPUT 
        self.rframe=Tkinter.LabelFrame(master=self.frame1, text="Data Panel")
        self.rframe.grid(row=6, columnspan=6, sticky='nswe')

        self.button5=Tkinter.Button(self.rframe, text="Protein", command=self.lift_prot_info)
        self.button5.grid(row=0, column=0)
        self.button6=Tkinter.Button(self.rframe, text="Ligands", command=self.lift_lig_info)
        self.button6.grid(row=0, column=1)
        
        self.button7=Tkinter.Button(self.rframe, text="PDB", command=self.lift_pdb_file)
        self.button7.grid(row=0, column=3)
             
        self.button8=Tkinter.Button(self.rframe, text="Uniprot", command=self.lift_uniprot_file)
        self.button8.grid(row=0, column=2)
        
        self.button9=Tkinter.Button(self.rframe, text="Pathways", command=self.lift_kegg_info)
        self.button9.grid(row=0, column=4)
        
        self.button10=Tkinter.Button(self.rframe, text="Similar Ligands", command=self.lift_ligss_info)
        self.button10.grid(row=0, column=5)      


        self.text1=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text1.grid(row=5, column=0, columnspan=10, stick='ns')
        
        scrollbar1=Tkinter.Scrollbar(self.rframe, command=self.text1.yview)
        scrollbar1.grid(row=5, column=11, sticky='nswe')
        self.text1.configure(yscrollcommand=scrollbar1.set)
        self.text1.lower()

        self.text2=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text2.grid(row=5, column=0, columnspan=10, stick='ns')
        self.text2.lower()

        self.text3=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text3.grid(row=5, column=0, columnspan=10, stick='ns')
        self.text3.lower()

        self.text4=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text4.grid(row=5, column=0, columnspan=10, stick='ns')
        self.text4.lower()

        self.text5=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text5.grid(row=5, column=0, columnspan=10, stick='ns')
        self.text5.lower()

        self.text6=Tkinter.Text(master=self.rframe, wrap=Tkinter.WORD)
        self.text6.grid(row=5, column=0, columnspan=10, stick='ns')
        self.text6.lower()
    def lift_prot_info(self):
        self.text1.lift()
        scrollbar1=Tkinter.Scrollbar(self.rframe, command=self.text1.yview)
        scrollbar1.grid(row=5, column=11, sticky='nswe')
        self.text1.configure(yscrollcommand=scrollbar1.set)
        self.text2.lower()
        self.text3.lower()
        self.text4.lower()
        self.text5.lower()
        self.text6.lower()
    def lift_lig_info(self):
        self.text1.lower()
        self.text2.lift()
        scrollbar2=Tkinter.Scrollbar(self.rframe, command=self.text2.yview)
        scrollbar2.grid(row=5, column=11, sticky='nswe')
        self.text2.configure(yscrollcommand=scrollbar2.set)
        self.text3.lower()
        self.text4.lower()
        self.text5.lower()
        self.text6.lower()
    def lift_pdb_file(self):
        self.text3.lift()
        scrollbar3=Tkinter.Scrollbar(self.rframe, command=self.text3.yview)
        scrollbar3.grid(row=5, column=11, sticky='nswe')
        self.text3.configure(yscrollcommand=scrollbar3.set)
        self.text1.lower()
        self.text2.lower()
        self.text4.lower()
        self.text5.lower()
        self.text6.lower()
    def lift_uniprot_file(self):
        self.text4.lift()
        scrollbar4=Tkinter.Scrollbar(self.rframe, command=self.text4.yview)
        scrollbar4.grid(row=5, column=11, sticky='nswe')
        self.text4.configure(yscrollcommand=scrollbar4.set)
        self.text1.lower()
        self.text2.lower()
        self.text3.lower()
        self.text5.lower()
        self.text6.lower()
    def lift_kegg_info(self):
        self.text5.lift()
        scrollbar5=Tkinter.Scrollbar(self.rframe, command=self.text5.yview)
        scrollbar5.grid(row=5, column=11, sticky='nswe')
        self.text5.configure(yscrollcommand=scrollbar5.set)
        self.text1.lower()
        self.text2.lower()
        self.text3.lower()
        self.text4.lower()
        self.text6.lower()
    def lift_ligss_info(self):
        self.text6.lift()
        scrollbar6=Tkinter.Scrollbar(self.rframe, command=self.text6.yview)
        scrollbar6.grid(row=5, column=11, sticky='nswe')
        self.text6.configure(yscrollcommand=scrollbar6.set)
        self.text1.lower()
        self.text2.lower()
        self.text3.lower()
        self.text4.lower()
        self.text5.lower()
    def file_upload(self):
        toplevel1 = Tkinter.Toplevel()
        toplevel1.withdraw()
        
        self.userpdbfile = tkFileDialog.askopenfile(parent=toplevel1,mode='rb',title='Choose a file')
        self.userpdbfile_path=self.userpdbfile.name
        print self.userpdbfile_path

        self.userpdb_filename=os.path.basename(self.userpdbfile_path)
        self.userpdb_filename_noext=self.userpdb_filename.split('.')[0]
        if self.userpdbfile != None:
            self.label4.config(text=self.userpdb_filename)
    def smiles_help(self):
        #dnlkd
        tkMessageBox.showinfo(title = 'Smiles', message = "To find similar ligands, paste your smile string in the entry box and hit Find Similar Ligands button. \n On Mac use Command+C to copy from the Data Panel and use Control+V to paste in the entry box")
    def showLink(self, event, arg):
        #fgdfg
        webbrowser.open_new(arg)
    def show_pathway(self, path):
        toplevel = Tkinter.Toplevel()
        #toplevel.grid(sticky='nswe')
        toplevel.columnconfigure(0, weight=1)
        toplevel.rowconfigure(0, weight=1)
        Tframe=Tkinter.Frame(toplevel)
        Tframe.grid(sticky='nswe')
        Tframe.columnconfigure(0, weight=1)
        Tframe.rowconfigure(0, weight=1)
        PathwayImage=Tkinter.PhotoImage(file=path)
        PhotoImage=Tkinter.Text(Tframe)
        PhotoImage.image_create(Tkinter.END, image=PathwayImage)
        PhotoImage.img=PathwayImage
        PhotoImage.grid(row = 0, column=0, sticky='nswe')
        scrollbar1=Tkinter.Scrollbar(Tframe, command=PhotoImage.yview)
        scrollbar1.grid(row=0, column=1, sticky='nswe')
        scrollbar2=Tkinter.Scrollbar(Tframe, orient=Tkinter.HORIZONTAL, command=PhotoImage.xview)
        scrollbar2.grid(row=1, column=0, sticky='nswe')
        PhotoImage.columnconfigure(0, weight=1)
        PhotoImage.rowconfigure(0, weight=1)
        PhotoImage.configure(yscrollcommand=scrollbar1.set)
        PhotoImage.configure(xscrollcommand=scrollbar2.set)
        PhotoImage.lift()
    def get_similar_ligands(self):
        self.ligssdir=os.path.join(self.outdir, "Similar_Ligands")
        if os.path.exists(self.ligssdir):
            os.chdir(self.ligssdir)
        else:
            os.mkdir(self.ligssdir)
            os.chdir(self.ligssdir)
        #print "Aquiring similar ligands...."
        self.smiles=self.entryVariable3.get()
        #print self.smiles        
        self.lift_ligss_info()
        url="https://www.ebi.ac.uk/chemblws/compounds/similarity/"+self.smiles+"/70"
        #print url
        try:
            self.text6.config(state=Tkinter.NORMAL)
            self.text6.delete(1.0, Tkinter.END)
            response_assay_xml=urllib2.urlopen(url).read()
            root=ET.fromstring(response_assay_xml)
            self.text6.insert(Tkinter.INSERT, "Similar Ligands: "+"\n\n")
            self.text6.insert(Tkinter.INSERT, "ChemblID \t Similarity \t smiles \n\n")
            fileh=open("Similar_Ligands.smi", "w")
            idh=open("Similar_ligands.txt", "w")
            idh.write("smiles \t ChemblID \t Similarity \n")
            for i in root:
                self.text6.insert(Tkinter.INSERT, i[1].text+"\t"+i[4].text+"\t"+i[0].text+"\n\n")
                fileh.write(i[0].text+"\n")
                idh.write(i[0].text+"\t"+i[1].text+"\t"+i[4].text+"\n")
            fileh.close()
            idh.close()
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for similar ligands!"
            elif err.code == 403:
                print "Access denied for similar ligands!"
            else:
                print "Something happened in similar ligands! Error code", err.code
    def get_smiles(self, chembl_id):
        print "Aquiring smiles....\n THIS COULD TAKE LONG TIME DEPENDING ON NUMBER OF MOLECULES THAT MATCHES CRITERION!!"
        #tkMessageBox.showinfo(title="Aquiring smiles...", message="THIS COULD TAKE LONG TIME DEPENDING ON NUMBER OF MOLECULES THAT MATCHES CRITERION!!")
        ids=chembl_id
        smiles=list()
        for i in ids:
            url="http://www.ebi.ac.uk/chemblws/compounds/"+str(i)
            try:
                response_ligsmi_xml=urllib2.urlopen(url).read()
                root=ET.fromstring(response_ligsmi_xml)              
                smiles.append(root[0].text)
            except urllib2.HTTPError, err:
                if err.code == 404:
                    print "Page not found for smiles!"
                elif err.code == 403:
                    print "Access denied for smiles!"
                else:
                    print "Something else happened in smiles! Error code", err.code
        return smiles
    def get_info(self):
        #print "1 Aquiring uniprot id from pdb id...."
        self.pdb_id=self.entryVariable1.get().upper()
        self.pdb_chain_id=self.entryVariable2.get().upper()
        cwd = os.path.expanduser("~/Desktop/")
        self.outdir = os.path.join(cwd, 'PyMine_Output_'+str(self.pdb_id))
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
            os.chdir(self.outdir)
        
        for line in urllib2.urlopen('http://www.uniprot.org/docs/pdbtosp.txt'):
            if len(line.split())>1:
                if self.pdb_id == str(line.split()[0]):
                    self.uniprot.append(str(line.split()[5])[1:-1])
        self.text1.insert(Tkinter.INSERT, "PDB ID: "+self.pdb_id+ "\n\n")
        if self.uniprot:
            self.text1.insert(Tkinter.END, "Uniprot: " +', '.join(map(str, self.uniprot))+"\n\n")        
        else:
            self.text1.insert(Tkinter.END, "Uniprot id not found " +"\n\n") 
    def get_user_info(self):
        #print "1 Aquiring uniprot id from pdb id...."
        self.pdb_id=self.userpdb_filename_noext
        print self.pdb_id
        #self.pdb_chain_id=self.entryVariable2.get().upper()
        cwd = os.path.expanduser("~/Desktop/")
        self.outdir = os.path.join(cwd, 'PyMine_Output_'+str(self.pdb_id))
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
            os.chdir(self.outdir)
        self.uniprot.append(self.entryVariable5.get().upper())
        self.text1.insert(Tkinter.INSERT, "PDB File: "+self.pdb_id+ "\n\n")
        if self.uniprot:
            self.text1.insert(Tkinter.END, "Uniprot: " +', '.join(map(str, self.uniprot))+"\n\n")        
        else:
            self.text1.insert(Tkinter.END, "Uniprot id not found " +"\n\n")
    def show_pdb(self):
        #print "2 Importing 3d structure...."
        pymol.cmd.cd(self.outdir)
        #print pymol.cmd.pwd()
        current_pdb=self.pdb_id
        #pymol.finish_launching()
        if self.flag==1:
            pymol.cmd.load(self.userpdbfile_path)
        else:
            pymol.cmd.fetch(current_pdb) #pymol.cmd.load("/Users/rrc/Desktop/pymol_plugin/2RH1.pdb",current_pdb)  

        pdbfilename=str(self.pdb_id)+".pdb"
        #pymol.cmd.save(pdbfilename, current_pdb)
        pymol.cmd.hide('everything', current_pdb)
        #pymol.cmd.select("selection", current_pdb)
        pymol.cmd.show('cartoon')
        pymol.cmd.select('ligand', 'organic')
    def get_pdb_file(self):
        #print "3 Aquiring pdb and uniprot file...."
        if self.flag==1:
            pdbfile=open(self.userpdbfile_path, "r")
            for line in pdbfile:
                self.text3.insert(Tkinter.END, line)
        else:
            filename=str(self.pdb_id.lower())+".pdb"
            pdbfile=open(filename, "r")
            for line in pdbfile:
                self.text3.insert(Tkinter.END, line)
    def get_uniprot_file(self):
        #print self.uniprot[0]
        if self.uniprot:
            fh=open(self.uniprot[0]+".txt", "w")
            for line in urllib2.urlopen('http://www.uniprot.org/uniprot/'+self.uniprot[0]+'.txt'):
                self.text4.insert(Tkinter.END, line)
                fh.write(line)
            fh.close()
        else:
            print "Error in uniprot id"
    def get_ligands(self):
        #print "4 Aquiring pdb ligands...."
        try:
            url="http://www.rcsb.org/pdb/rest/ligandInfo?structureId="+self.pdb_id
            response_xml = urllib2.urlopen(url).read()
            root=ET.fromstring(response_xml)
            for i in root[0]:
                chemid = i.attrib['chemicalID']
                for j in i:
                    if j.tag=="smiles":
                        smiles=j.text
                    if j.tag=="chemicalName":
                        chem_name=j.text
                self.ligands.append([chemid, chem_name, smiles]) 
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for pdb ligands!"
            elif err.code == 403:
                print "Access denied for pdb ligands!"
            else:
                print "Something else happened in pdb ligands! Error code", err.code
        
        if self.ligands:
            self.text2.insert(Tkinter.END, "Ligands in PDB: \n\n")
            for i in self.ligands:
                self.text2.insert(Tkinter.END, ' '.join(map(str, i))+"\n\n")
        else:
            self.text2.insert(Tkinter.END, "Ligands not found\n\n")
    def get_ligand_images(self):
        #print "5 Aquiring pdb ligand images...."
        self.ligdir=os.path.join(self.outdir, "Ligands")
        if not os.path.exists(self.ligdir):
            os.mkdir(self.ligdir)
            os.chdir(self.ligdir)
            
        if self.ligands:    
            for i in self.ligands:
                chid=i[0]
                #print "Working on "+ str(chid)
                try:
                    url="http://www.ebi.ac.uk/chemblws/compounds/smiles/"+i[2] 
                    #print url
                    response_xml_chemblids=urllib2.urlopen(url).read()
                    root=ET.fromstring(response_xml_chemblids)
                    if len(root)>0:
                        lig_chemblID=root[0].find("chemblId").text
                        self.ligand_chemblid.append([chid, lig_chemblID])
                except urllib2.HTTPError, err:
                    if err.code == 404:
                        print "Page not found for ligand images!"
                    elif err.code == 403:
                        print "Access denied for ligand images!"
                    else:
                        print "Ignored smiles retrieval for ions!"
        else:
            print "Ligands not present"
        if self.ligand_chemblid:
            for i in self.ligand_chemblid:
                url="http://www.ebi.ac.uk/chemblws/compounds/"+i[1]+"/image" 
                #print url
                imgRequest = urllib2.Request(url)
                imgData=urllib2.urlopen(imgRequest).read()
                self.ligand_images.append(imgData) 
                fh=open(str(i[1])+".gif", "w")
                fh.write(imgData)
                fh.close()
        else:
            print "Ligand chembl id not found"
    def get_target_chembl_id(self):
        #print "6 Aquiring target chembl id...."
        if self.uniprot:
            url="http://www.ebi.ac.uk/chemblws/targets/uniprot/"+str(self.uniprot[0])
            #print url
            try:
                response_assay_xml=urllib2.urlopen(url).read()
                root=ET.fromstring(response_assay_xml)
                for i in root:
                    #print i.tag
                    if i.tag =="preferredName":
                        self.common_name=str(i.text)
                    if i.tag =="organism":
                        self.organism=str(i.text)
                    if i.tag=="chemblId":
                        self.target_chemblID=i.text
            except urllib2.HTTPError, err:
                if err.code == 404:
                    print "Page not found for target chembl id!"
                elif err.code == 403:
                    print "Access denied for target chembl id!"
                else:
                    print "Something happened in target chembl id! Error code", err.code
        else:
            print "Error in uniprot id!"
            self.text2.insert(Tkinter.END, "Could not retrieve assay information because uniprot id missing\n\n")

        if self.target_chemblID:
            #print self.target_chemblID
            self.get_assay_info()
            if self.ec50_comps:
                #print "EC50 data available"
                self.text2.insert(Tkinter.END, "Compounds with EC50 values <=100 nM:"+"\n\n")
                self.text2.insert(Tkinter.END, ' '.join(map(str, self.ec50_comps))+"\n\n")
            else:
                self.text2.insert(Tkinter.END, "EC50 data not available"+"\n\n")
            if self.ic50_comps:
                #print "IC50 data available"
                self.text2.insert(Tkinter.END, "Compounds with IC50 values <=100 nM:"+"\n\n")
                self.text2.insert(Tkinter.END, ' '.join(map(str, self.ic50_comps))+"\n\n")
            else:
                self.text2.insert(Tkinter.END, "IC50 data not avaialble"+"\n\n")
            if self.ki_comps:
                #print "KI data available"
                self.text2.insert(Tkinter.END, "Compounds with Ki values <=100 nM:"+"\n\n")
                self.text2.insert(Tkinter.END, ' '.join(map(str, self.ki_comps))+"\n\n")
            else:
                self.text2.insert(Tkinter.END, "Ki data not available"+"\n\n")
        else:
            self.text2.insert(Tkinter.END, "Assay data not available"+"\n\n")
    def get_approved_drugs(self):
        #print "7 Aquiring approved drugs...."
        try:
            url="http://www.ebi.ac.uk/chemblws/targets/"+self.target_chemblID+"/approvedDrug"
            response_approved_xml=urllib2.urlopen(url).read()
            root=ET.fromstring(response_approved_xml)
            for i in root:
                molecule =list()
                if len(i)==0:
                    break
                else:
                    for j in i:
                        molecule.append([j.tag, j.text])
                self.approved_drugs.append(molecule)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for approved drugs!"
            elif err.code == 403:
                print "Access denied for approved drugs!"
            else:
                print "Something happened in aquiring approved_drugs! Error code", err.code
    def show_lig_info(self):
        #print "8 Showing approved drug information...."
        os.chdir(self.ligdir)
        self.agonist=list()
        self.antagonist=list()
        if not self.approved_drugs:
            self.text2.insert(Tkinter.END, "No Approved Drugs found for this receptor"+"\n\n")
        else:
            self.text2.insert(Tkinter.END, "Approved Drugs: \n\n")
            for i in self.approved_drugs:
                #print i[2][1].split()[-1] 
                if i[2][1].split()[-1] == "agonist":
                    self.agonist.append([i])
                if i[2][1].split()[-1] =="antagonist":
                    self.antagonist.append([i]) 
            #self.text2.insert(Tkinter.END, ''.join(map(str, self.approved_drugs))+"\n\n")
            if self.agonist:
                self.text2.insert(Tkinter.END, "Agonists: \n\n")
                for i in self.agonist:
                    for j in i:
                        for k in j:
                            self.text2.insert(Tkinter.END, ' '.join(map(str, k))+"\n")
                    self.text2.insert(Tkinter.END, "\n\n")
            if self.antagonist:
                self.text2.insert(Tkinter.END, "Antagonists: \n\n")
                for i in self.antagonist:
                    for j in i:
                        for k in j:
                            self.text2.insert(Tkinter.END, ' '.join(map(str, k))+"\n")
                    self.text2.insert(Tkinter.END, "\n\n")                
        if self.agonist:
            fh=open("Approved_agonist.txt", "w")
            for i in self.agonist:
                for j in i:
                    fh.write(str(j[0][1]+"\n"))
            fh.close()
        if (self.antagonist):
            fh=open("Approved_antagonist.txt", "w")
            for i in self.antagonist:
                for j in i:
                    fh.write(str(j[0][1]+"\n"))
            fh.close()    
    def get_saps(self):
        #print "9 Aquiring saps...."
        for line in urllib2.urlopen('http://www.uniprot.org/docs/humsavar.txt'):
            if len(line.split())>1:
                if str(self.uniprot[0]) == str(line.split()[1]):
                    gene_name=line.split()[0]
                    mutation=line.split()[3][2:]
                    origres=mutation[:3]
                    num=mutation[3:-3]
                    changedres=mutation[-3:]
                    disease=line.split()[6:]
                    self.saps.append([origres, num, changedres, disease])
                    #print gene_name, mutation, origres, num, changedres
        if self.saps:
            self.show_saps()
            self.text1.insert(Tkinter.END, "Single Amino Acid Polymoprphism:\n\n"+  '\n'.join(map(str, self.saps))+"\n\n")
        else:
            print "SAPs not found"
            self.text1.insert(Tkinter.END, "Single Amino Acid Polymoprphism not found"+"\n\n")
    def show_saps(self):
        #print "10 Showing SAPS...."
        sap_residues=list()
        sap_res_str=''
        for i in self.saps:
            if i[1] not in sap_residues:
                sap_residues.append(i[1])
        for i in sap_residues:
            sap_res_str="resi " + str(i)
            #print sap_res_str
            pymol.cmd.select("SAPs", sap_res_str)
            pymol.cmd.show("spheres", sap_res_str)
            pymol.cmd.deselect()
    def get_bs(self):
        #print "11 Aquiring binding site information...."
        lig_bs=list()
        ppi_bs=list()
        dna_bs=list()
        rna_bs=list()
        ion_bs=list()
        pep_bs=list()    
        try:
            for line in urllib2.urlopen("https://dl.dropboxusercontent.com/u/4882263/ibisdown/"+self.pdb_id[1:-1]+"/"+self.pdb_id+".txt"):
                spline=line.split(":") #Query:Interaction_type:Mmdb_Residue_No:PDB_Residue_No:Binding_Site_Residues:Binding_Site_Conservation:Avg_PercentID:Singleton:PISA_validation:Biol_Chemical_validation:Site_CDD_Annotation:Interaction_Partner:PDB_Evidence:Is_Observed:Ranking_Score:Query_Domain
                if spline[1]=="LIG" and spline[0][-1:]==self.pdb_chain_id:
                    lig_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
                if spline[1]=="PPI" and spline[0][-1:]==self.pdb_chain_id:
                    ppi_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
                if spline[1]=="DNA" and spline[0][-1:]==self.pdb_chain_id:
                    dna_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
                if spline[1]=="RNA" and spline[0][-1:]==self.pdb_chain_id:
                    rna_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
                if spline[1]=="ION" and spline[0][-1:]==self.pdb_chain_id:
                    ion_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
                if spline[1]=="PEP" and spline[0][-1:]==self.pdb_chain_id:
                    pep_bs.append([spline[1], spline[0], spline[3], spline[11], spline[12]])
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for binding sites!"
            elif err.code == 403:
                print "Access denied for binding sites!"
            else:
                print "Something else happened in getting binding site information! Error code", err.code
                
        self.binding_sites=[lig_bs, ppi_bs, dna_bs, rna_bs, ion_bs, pep_bs]
    def show_bs(self):
        #print "12 Showing binding sites...."
        counter=0
        for i in self.binding_sites[0]:
            counter+=1
            self.lig_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("lig_bs"+str(counter), self.lig_bs_residues)
            pymol.cmd.deselect()
        pymol.cmd.group("Ligand_Binding_Sites", "lig_bs*")
        
        counter=0
        for i in self.binding_sites[1]:
            counter+=1
            self.ppi_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("ppi_bs"+str(counter), self.ppi_bs_residues)    #pymol.cmd.create() would create objects instead of selection for coloring
            pymol.cmd.deselect()
        pymol.cmd.group("PPI_Sites", "ppi_bs*")    
        
        counter=0
        for i in self.binding_sites[2]:
            counter+=1
            self.dna_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("dna_bs"+str(counter), self.dna_bs_residues)    #pymol.cmd.create() would create objects instead of selection for coloring
            pymol.cmd.deselect()
        pymol.cmd.group("DNA_Binding_Sites", "dna_bs*")

        counter=0
        for i in self.binding_sites[3]:
            counter+=1
            self.rna_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("rna_bs"+str(counter), self.rna_bs_residues)    #pymol.cmd.create() would create objects instead of selection for coloring
            pymol.cmd.deselect()
        pymol.cmd.group("RNA_Binding_Sites", "rna_bs*")

        counter=0
        for i in self.binding_sites[4]:
            counter+=1
            #print counter
            self.ion_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("ion_bs"+str(counter), self.ion_bs_residues)    #pymol.cmd.create() would create objects instead of selection for coloring
            pymol.cmd.deselect()
        pymol.cmd.group("ION_Bindins_Sites", "ion_bs*")

        counter=0
        for i in self.binding_sites[5]:
            counter+=1
            self.pep_bs_residues="resi "+ ','.join(map(str, i[2].lstrip().split(' ')))
            pymol.cmd.select("pep_bs"+str(counter), self.pep_bs_residues)    #pymol.cmd.create() would create objects instead of selection for coloring
            pymol.cmd.deselect()
        pymol.cmd.group("PEP_Binding_Sites", "pep_bs*")

        if len(self.binding_sites[0])==0 and len(self.binding_sites[1])==0 and len(self.binding_sites[2])==0 and len(self.binding_sites[3])==0 and len(self.binding_sites[4])==0 and len(self.binding_sites[5])==0:
            self.text1.insert(Tkinter.END, "Binding site data not found\n")
        else:
            self.text1.insert(Tkinter.END, "Binding Sites/Similar Binding Sites: \n\n")
            for i in self.binding_sites:
                for j in i:
                    self.text1.insert(Tkinter.END, '\t'.join(map(str, j))+"\n\n")
    def get_assay_info(self):
        #print "13 Aquiring assay information...."
        self.ligdir=os.path.join(self.outdir, "Ligands")
        if not os.path.exists(self.ligdir):
            os.mkdir(self.ligdir)
            os.chdir(self.ligdir)
        #os.chdir(self.ligdir)
        url="http://www.ebi.ac.uk/chemblws/targets/"+self.target_chemblID+"/bioactivities"  
        try:
            response_xml_chemblids=urllib2.urlopen(url).read()
            root=ET.fromstring(response_xml_chemblids)
            for i in root:
                if i[6].text=="EC50" and i[13].text=="=" and i[12].text!="Unspecified" and float(i[12].text)<=0.1 and i[9].text=="nM":
                    self.ec50_comps.append(i[4].text)
                elif i[6].text=="IC50" and i[13].text=="=" and i[12].text!="Unspecified" and float(i[12].text)<=10 and i[9].text=="nM":
                    self.ic50_comps.append(i[4].text)
                elif i[6].text=="Ki" and i[13].text=="=" and i[12].text!="Unspecified" and float(i[12].text)<=10 and i[9].text=="nM":
                    self.ki_comps.append(i[4].text)
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for assay data!"
            elif err.code == 403:
                print "Access denied for assay data!"
            else:
                print "Something else happened in get_assay_info! Error code", err.code
        if self.ec50_comps:
            #print self.ec50_comps
            #print "EC50 data available"
            ec50_fh=open("EC50.txt", "w")
            for i in self.ec50_comps:
                ec50_fh.write(str(i)+"\n")
            ec50_fh.close()
            ec50_smi=self.get_smiles(self.ec50_comps)
            if ec50_smi:
                ec50smi_fh=open("EC50.smi", "w")
                ec50smi_fh.write('\n'.join(map(str, ec50_smi)))
                ec50smi_fh.close()
        else:
            print "EC50 data not available"
        if self.ic50_comps:
            #print "IC50 data available"
            ic50_fh=open("IC50.txt", "w")
            for i in self.ic50_comps:
                ic50_fh.write(str(i)+"\n")
            ic50_fh.close()
            ic50_smi=self.get_smiles(self.ic50_comps)
            if ic50_smi:
                ic50smi_fh=open("IC50.smi", "w")
                ic50smi_fh.write('\n'.join(map(str, ic50_smi)))
                ic50smi_fh.close()
        else:
            print "IC50 data not available"
        if self.ki_comps:
            #print "Ki data available"
            ki_fh=open("KI.txt", "w")
            for i in self.ki_comps:
                ki_fh.write(str(i)+"\n")
            ki_fh.close()
            
            ki_smi=self.get_smiles(self.ki_comps)
            if ki_smi:
                ki_smi_fh=open("KI.smi", "w")
                ki_smi_fh.write('\n'.join(map(str, ki_smi)))
                ki_smi_fh.close()
        else:
            print "Ki data not available"
    def get_kegg_info(self):
        #print "15 Aquiring pathway information...."
        #print os.getcwd()
        url = 'http://rest.genome.jp/link/genes/uniprot:'+self.uniprot[0]+'/original'
        #print "Aquiring genes...."
        self.kegg_genes=list()
        try:
            response = urllib2.urlopen(url)
            for line in response:
                self.kegg_genes.append(line.split()[1])
            """
            for i in self.kegg_genes:
                self.text5.insert(Tkinter.INSERT, str(i)+ "\n\n")
            """
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found for genes!"
            elif err.code == 403:
                print "Access denied for genes!"
            else:
                print "Something happened in Kegg genes! Error code", err.code
        
        #### genes to pathway ids
        if self.kegg_genes:
            for i in self.kegg_genes:
                url = 'http://rest.genome.jp/link/path/'+i+'/original'
                #print "Aquiring kegg pathaway id...."
                self.kegg_pathway_ids=list()
                try:
                    response = urllib2.urlopen(url)
                    for line in response:
                        self.kegg_pathway_ids.append(line.split()[1])
                except urllib2.HTTPError, err:
                    if err.code == 404:
                        print "Page not found for pathway ids!"
                    elif err.code == 403:
                        print "Access denied!"
                    else:
                        print "Something happened in Kegg pathway ids! Error code", err.code
                
                ### get pathway information
                if self.kegg_pathway_ids:
                    for i in self.kegg_pathway_ids:
                        url= 'http://rest.kegg.jp/get/'+i
                        #print "Aquiring Kegg Pathways...."
                        try:
                            response = urllib2.urlopen(url)
                            for line in response:
                                if line.startswith('CLASS'):
                                    break
                                self.text5.insert(Tkinter.INSERT, line +"\n")

                            # For the pathway information hyperlink
                            self.text5.insert(Tkinter.INSERT, url+"\n\n", ('link'))
                            self.text5.tag_config('link', foreground="blue", underline=1)
                            self.text5.tag_bind('link', '<Button-1>', lambda event, arg=url: self.showLink(event, arg))
                            
                        except urllib2.HTTPError, err:
                            if err.code == 404:
                                print "Page not found for kegg pathways!"
                            elif err.code == 403:
                                print "Access denied for kegg pathways!"
                            else:
                                print "Something happened in Kegg pathways! Error code", err.code
                        ### Get pathway images
                        url= 'http://rest.kegg.jp/get/'+i+'/image'
                        #print "Aquiring pathaway images...."
                        try:
                            imgRequest = urllib2.Request(url)
                            imgData=urllib2.urlopen(imgRequest).read()
                            self.pathwaydir=os.path.join(self.outdir, "Pathways")
                            if os.path.exists(self.pathwaydir):
                                os.chdir(self.pathwaydir)
                            else:
                                os.mkdir(self.pathwaydir)
                                os.chdir(self.pathwaydir)
                            filename=i.split(':')[1]
                            fh=open(filename+".gif", "w")
                            fh.write(imgData)
                            fh.close()
                            path_image=self.pathwaydir+"/"+filename+".gif"
                            #print path_image
                            
                            ButtonImage=Tkinter.PhotoImage(file=path_image)
                            #print ButtonImage
                            path_button=Tkinter.Button(self.text5, text="Pathway Image", command=lambda j=path_image: self.show_pathway(j))
                            #path_button.img=ButtonImage
                            self.text5.window_create(Tkinter.INSERT, window=path_button)
                            self.text5.insert(Tkinter.INSERT, "\n----------------------------X--------------------------\n\n\n")
                        except urllib2.HTTPError, err:
                            if err.code == 404:
                                print "Page not found for pathway images!"
                            elif err.code == 403:
                                print "Access denied for pathway images!"
                            else:
                                print "Something happened in Kegg pathway images! Error code", err.code
                else:
                    print "Kegg pathway ids not found"
                    self.text5.insert(Tkinter.INSERT, "Kegg data not found.\n\n")        
        else:
            print "Kegg gene not available"
            self.text5.insert(Tkinter.INSERT, "Kegg data not found.\n\n")
        #print os.getcwd()
    def get_results(self):
        self.text1.lift()
        self.text1.config(state=Tkinter.NORMAL)
        self.text1.delete(1.0, Tkinter.END)
        self.text2.config(state=Tkinter.NORMAL)
        self.text2.delete(1.0, Tkinter.END)
        self.text3.config(state=Tkinter.NORMAL)
        self.text3.delete(1.0, Tkinter.END)
        self.text4.config(state=Tkinter.NORMAL)
        self.text4.delete(1.0, Tkinter.END)
        self.text5.config(state=Tkinter.NORMAL)
        self.text5.delete(1.0, Tkinter.END)
        self.text6.config(state=Tkinter.NORMAL)
        self.text6.delete(1.0, Tkinter.END)

        if self.userpdbfile!=None and self.entryVariable5.get()!=None:
            self.flag=1
            self.get_user_info()
            self.show_pdb()
            self.get_pdb_file()
            self.get_uniprot_file()
            self.get_target_chembl_id()
            self.get_approved_drugs()
            self.show_lig_info()        
            self.get_saps()     
            #self.get_bs()
            #self.show_bs()
            self.get_kegg_info()
        else:
            self.get_info()
            self.show_pdb()
            self.get_pdb_file()
            self.get_uniprot_file()
            self.get_ligands()
            self.get_ligand_images()
            self.get_target_chembl_id()
            self.get_approved_drugs()
            self.show_lig_info()        
            self.get_saps()     
            self.get_bs()
            self.show_bs()
            self.get_kegg_info()

        self.text1.config(state=Tkinter.DISABLED)
        self.text2.config(state=Tkinter.DISABLED)
        self.text3.config(state=Tkinter.DISABLED)
        self.text4.config(state=Tkinter.DISABLED) 
        self.text5.config(state=Tkinter.DISABLED)
        self.text6.config(state=Tkinter.DISABLED)
    def clear(self):
        #Clear All the variables so that if we change the pdbid it will recreate the screen.
        self.text1.config(state=Tkinter.NORMAL)
        self.text1.delete(1.0, Tkinter.END)
        self.text2.config(state=Tkinter.NORMAL)
        self.text2.delete(1.0, Tkinter.END)
        self.text3.config(state=Tkinter.NORMAL)
        self.text3.delete(1.0, Tkinter.END)
        self.text4.config(state=Tkinter.NORMAL)
        self.text4.delete(1.0, Tkinter.END)
        self.text5.config(state=Tkinter.NORMAL)
        self.text5.delete(1.0, Tkinter.END)
        self.text6.config(state=Tkinter.NORMAL)
        self.text6.delete(1.0, Tkinter.END)

        
        self.flag=0
        self.pdb_id=''
        self.pdb_chain_id=''
        self.entryVariable1.set('')
        self.entryVariable2.set('')
        self.entryVariable3.set('')
        self.entryVariable5.set(None)
        self.userpdbfile=None
        self.userpdbfile_path=''
        self.userpdb_filename=''
        self.userpdb_filename_noext=''
        self.label4.config(text='')
        cwd=os.path.expanduser("~/Desktop/")
        self.pdb_file=''
        self.smiles=''
        self.name=list()
        self.summary=list()
        self.symbol=list()
        self.uniprot=list()
        self.binding_sites=list()
        self.ppi_bs_residues=''
        self.lig_bs_residues=''
        self.dna_bs_residues=''
        self.rna_bs_residues=''
        self.ion_bs_residues=''
        self.pep_bs_residues=''
        self.pathways=list()
        self.saps=list()
        self.ligands=list()
        self.ligand_chemblid=list()
        self.ligand_images=list()
        self.agonist=list()
        self.antagonist=list()
        self.ki_comps=list()
        self.ec50_comps=list()
        self.ic50_comps=list()
        self.outdir=None
        pdbfile=None
        pymol.cmd.delete('all')
        pymol.cmd.reinitialize()
        self.text1.lift()
def main():
    app = PyMine(None)
    app.title('PyMine Data Integration')
    app.mainloop()
if __name__ == "__main__":
        main()