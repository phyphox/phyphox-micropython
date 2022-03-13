from io import StringIO

phyphoxBleNViews      = 5
phyphoxBleNElements   = 5
phyphoxBleNExportSets = 5

class PhyphoxBleExperiment:
    def __init__(self):
      self._TITLE          = "phyphox-Experiment"
      self._CATEGORY       = "phyphox mpy Experiments"
      self._DESCRIPTION    = "An experiment created with the phyphox BLE library for mpy-compatible micro controllers"
      self._CONFIG         = "000000"
      self._VIEWS          = [0]*phyphoxBleNViews
      self._EXPORTSETS     = [0]*phyphoxBleNExportSets
    
    @property
    def TITLE(self):
      return self._TITLE
    
    def CATEGORY(self):
      return self._CATEGORY
    
    def DESCRIPTION(self):
      return self._DESCRIPTION
    
    def CONFIG(self):
      return self._CONFIG
    
    def VIEWS(self):
      return self._VIEWS
    
    def EXPORTSETS(self):
      return self._EXPORTSETS
    
    def setTitle(self, strInput):
        self._TITLE = strInput
        
    def setCategory(self, strInput):
        self._CATEGORY = strInput
        
    def setDescription(self, strInput):
        self._DESCRIPTION = strInput
        
    def setConfig(self, strInput):
        self._CONFIG = strInput
    
    def getFirstBytes(self, buffer, device_name):
      errors = 0
      #header
      buffer.write('<phyphox version=\"1.10\">\n')
      #title
      buffer.write('<title>')
      buffer.write(self._TITLE)
      buffer.write('</title>\n')
      #category
      buffer.write('<category>')
      buffer.write(self._CATEGORY)
      buffer.write('</category>\n')
      #description
      buffer.write('<description>')
      buffer.write(self._DESCRIPTION)
      buffer.write('</description>\n')
      #container
      buffer.write('<data-containers>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH1</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH2</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH3</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH4</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH5</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH0</container>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CB1</container>\n')
      buffer.write('</data-containers>\n')
      #input
      buffer.write('<input>\n')
      buffer.write('\t<bluetooth name=\"')
      buffer.write(device_name)
      buffer.write('\" id=\"phyphoxBLE\" mode=\"notification\" rate=\"1\" subscribeOnStart=\"false\">\n')
      #config
      buffer.write('\t\t<config char=\"cddf1003-30f7-4671-8b43-5e40ba53514a\" conversion=\"hexadecimal\">')
      buffer.write(self._CONFIG)
      buffer.write('</config>\n\t\t')
      for i in range(5):
        buffer.write('<output char=\"cddf1002-30f7-4671-8b43-5e40ba53514a\" conversion=\"float32LittleEndian\" ')
        k = i*4
        tmp = "offset=\"%i\" >CH%i" % (k,i+1)
        buffer.write(tmp)
        buffer.write('</output>\n\t\t')
      buffer.write('<output char=\"cddf1002-30f7-4671-8b43-5e40ba53514a\" extra=\"time\">CH0</output>\n')
      buffer.write('\t</bluetooth>\n')
      buffer.write('</input>\n')
      #output
      buffer.write('<output>\n')
      buffer.write('\t<bluetooth name=\"')
      buffer.write(device_name)
      buffer.write('\" id=\"phyphoxBLE\">\n')
      buffer.write('\t\t<input char=\"cddf1003-30f7-4671-8b43-5e40ba53514a\" conversion=\"float32LittleEndian\">CB1</input>\n')
      buffer.write('\t</bluetooth>\n')
      buffer.write('</output>\n')
      #analysis
      buffer.write('<analysis sleep=\"0\"  onUserInput=\"false\"></analysis>\n')
      #views
      buffer.write('<views>\n')
      #errorhandling
      for i in range(phyphoxBleNViews):
        for j in range(phyphoxBleNElements):
          if self._VIEWS[i] and errors <= 2:
            if self._VIEWS[i]._ELEMENTS[j]:
              if not (self._VIEWS[i]._ELEMENTS[j]._ERROR._MESSAGE is ""):
                if errors == 0:
                  buffer.write('\t<view label=\"ERRORS\"> \n')
                self._VIEWS[i]._ELEMENTS[j]._ERROR.getBytes(buffer)
                errors += 1
      if errors > 0:
        buffer.write('\t\t<info  label=\"DE: Siehe Dokumentation für mehr Informationen zu Fehlern.\">\n')
        buffer.write('\t\t</info>\n')
        buffer.write('\t\t<info  label=\"EN: Please check the documentation for more information about errors.\">\n')
        buffer.write('\t\t</info>\n')
        buffer.write('\t</view>\n')
      
    def getViewBytes(self, buffer, v, e):
      if self._VIEWS[v] and v < phyphoxBleNViews:
        self._VIEWS[v].getBytes(buffer,e)
        
    def getLastBytes(self, buffer):
      noExports = True
      buffer.write('</views>\n')      
      #build export
      buffer.write('<export>\n')
      for i in range(phyphoxBleNExportSets):
        if self._EXPORTSETS[i]:
          self._EXPORTSETS[i].getBytes(buffer)
          noExports = False
      if noExports:
        buffer.write('\t<set name=\"mySet\">\n')
        buffer.write('\t\t<data name=\"myData1\">CH1</data>\n')
        buffer.write('\t\t<data name=\"myData2\">CH2</data>\n')
        buffer.write('\t\t<data name=\"myData3\">CH3</data>\n')
        buffer.write('\t\t<data name=\"myData4\">CH4</data>\n')
        buffer.write('\t\t<data name=\"myData5\">CH5</data>\n')
        buffer.write('\t</set>\n')
      buffer.write('</export>\n')
      buffer.write('</phyphox>')
      #print(buffer.getvalue())
              
    def addView(self, v):
      for i in range(phyphoxBleNViews):
        if not self._VIEWS[i]:
          self._VIEWS[i] = v
          break
        
    def addExportSet(self, e):
        for i in range(phyphoxBleNExportSets):
            if not self._EXPORTSETS[i]:
                self._EXPORTSETS[i] = e
                break
    
    class View:
      def __init__(self):
        self._LABEL         = ""
        self._XMLATTRIBUTE  = ""
        self._ELEMENTS = [0]*phyphoxBleNElements
        
      @property
      def LABEL(self):
        return self._LABEL
    
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
    
      def ELEMENTS(self):
        return self._ELEMENTS
    
      def addElement(self, e):
        for i in range(phyphoxBleNElements):
          if not self._ELEMENTS[i]:
            self._ELEMENTS[i] = e
            break
    
    
      def setLabel(self, strInput):
        self._LABEL = " label=\"" + strInput + "\""
    
      def setXMLAttribute(self, strInput):
        self._XMLATTRIBUTE = " " + strInput
      
      def getBytes(self, buffer, elem):
        if elem == 0:
          buffer.write('\t<view')
          buffer.write(self._LABEL)
          buffer.write(self._XMLATTRIBUTE)
          buffer.write('>\n')
        if self._ELEMENTS[elem]:
            self._ELEMENTS[elem].getBytes(buffer)
        if elem == phyphoxBleNElements-1:
          buffer.write('\t</view>\n')
    
    class Error:
      def __init__(self):
        self._MESSAGE       = ""
      
      @property
      def MESSAGE(self):
        return self._MESSAGE
    
      def getBytes(self, buffer):
        buffer.write('\t\t<info  label=\"ERROR FOUND: ')
        buffer.write(self._MESSAGE)
        buffer.write('\" color=\"ff0000\">\n')
        buffer.write('\t\t</info>\n')
    
    class Errorhandler:
      def __init__(self):
        pass
    
      def err_check_length(self, strInput1, intInput, strInput2):
        ret = PhyphoxBleExperiment.Error()
        if len(strInput1) > intInput:
          ret._MESSAGE += "ERR_01, in "
          ret._MESSAGE += strInput2
          ret._MESSAGE += "()."
        return ret
        
      def err_check_upper(self, intInput1, intInput2, strInput):
        ret = PhyphoxBleExperiment.Error()
        if intInput1 > intInput2:
          ret._MESSAGE += "ERR_02, in "
          ret._MESSAGE += strInput
          ret._MESSAGE += "()."
        return ret
        
      def err_check_hex(self, strInput1, strInput2):
        ret = PhyphoxBleExperiment.Error()
        if len(strInput1) != 6:
          ret._MESSAGE += "ERR_03, in "
          ret._MESSAGE += strInput2
          ret._MESSAGE += "()."
          return ret
        for i in strInput1:
          if i not in '0123456789abcdefABCDEF':
            ret._MESSAGE += "ERR_03, in "
            ret._MESSAGE += strInput2
            ret._MESSAGE += "()."
        return ret
        
      def err_check_style(self, strInput1, strInput2):
        ret = PhyphoxBleExperiment.Error()
        if not((strInput1 is "lines") or (strInput1 is "dots") or (strInput1 is "vbars") or (strInput1 is "hbars") or (strInput1 is "map")):
          ret._MESSAGE += "ERR_04, in "
          ret._MESSAGE += strInput2
          ret._MESSAGE += "()."
        return ret
    
    
    class Element(Errorhandler):
      def __init__(self):
        super().__init__()
        self._TYPEID        = 0
        self._LABEL         = ""
        self._ERROR         = PhyphoxBleExperiment.Error()
      
      @property
      def TYPEID(self):
        return self._TYPEID
        
      def LABEL(self):
        return self._LABEL
    
      def ERROR(self):
        return self._ERROR
    
      def setLabel(self, strInput):
        self._ERROR = self.err_check_length(strInput,41,'setLabel') if self._ERROR._MESSAGE is "" else self._ERROR
        self._LABEL = " label=\"" + strInput + "\""      
      
    class Graph(Element):
      def __init__(self):
        super().__init__()
        self._UNITX         = ""
        self._UNITY         = ""
        self._LABELX        = ""
        self._LABELY        = ""
        self._COLOR         = ""
        self._XPRECISION    = ""
        self._YPRECISION    = ""
        self._INPUTX        = "CH0"
        self._INPUTY        = "CH1"
        self._STYLE         = ""
        self._XMLATTRIBUTE  = ""
       
      @property
      def UNITX(self):
        return self._UNITX
        
      def UNITY(self):
        return self._UNITY
        
      def LABELX(self):
        return self._LABELX
        
      def LABELY(self):
        return self._LABELY
        
      def COLOR(self):
        return self._COLOR
        
      def XPRECISION(self):
        return self._XPRECISION
        
      def YPRECISION(self):
        return self._YPRECISION
        
      def INPUTX(self):
        return self._INPUTX
        
      def INPUTY(self):
        return self._INPUTY
        
      def STYLE(self):
        return self._STYLE
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
        
        
        
      def setUnitX(self, strInput):
        self._ERROR = self.err_check_length(strInput,5,'setUnitX') if self._ERROR._MESSAGE is "" else self._ERROR
        self._UNITX = " unitX=\"" + strInput + "\""
       
      def setUnitY(self, strInput):
        self._ERROR = self.err_check_length(strInput,5,'setUnitY') if self._ERROR._MESSAGE is "" else self._ERROR
        self._UNITY = " unitY=\"" + strInput + "\""
        
      def setLabelX(self, strInput):
        self._ERROR = self.err_check_length(strInput,20,'setLabelX') if self._ERROR._MESSAGE is "" else self._ERROR
        self._LABELX = " labelX=\"" + strInput + "\""
        
      def setLabelY(self, strInput):
        self._ERROR = self.err_check_length(strInput,20,'setLabelY') if self._ERROR._MESSAGE is "" else self._ERROR
        self._LABELY = " labelY=\"" + strInput + "\""
        
      def setColor(self, strInput):
        self._ERROR = self.err_check_hex(strInput,'setColor') if self._ERROR._MESSAGE is "" else self._ERROR
        self._COLOR = " color=\"" + strInput + "\""
        
      def setXPrecision(self, intInput):
        self._ERROR = self.err_check_upper(intInput,9999,'setXPrecision') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XPRECISION = " xPrecision=\"" + str(intInput) + "\""
        
      def setYPrecision(self, intInput):
        self._ERROR = self.err_check_upper(intInput,9999,'setYPrecision') if self._ERROR._MESSAGE is "" else self._ERROR
        self._YPRECISION = " yPrecision=\"" + str(intInput) + "\""
        
      def setChannel(self, intInputX, intInputY):
        self._ERROR = self.err_check_upper(intInputX,5,'setChannel') if self._ERROR._MESSAGE is "" else self._ERROR
        self._ERROR = self.err_check_upper(intInputY,5,'setChannel') if self._ERROR._MESSAGE is "" else self._ERROR
        self._INPUTX = "CH" + str(intInputX)
        self._INPUTY = "CH" + str(intInputY)
        
      def setStyle(self, strInput):
        self._ERROR = self.err_check_style(strInput,'setStyle') if self._ERROR._MESSAGE is "" else self._ERROR
        self._STYLE = " style=\"" + strInput + "\""
        
      def setXMLAttribute(self, strInput):
        self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XMLATTRIBUTE = " " + strInput
      
      def getBytes(self, buffer):
        buffer.write('\t\t<graph')
        buffer.write(self._LABEL)
        buffer.write(self._LABELX)
        buffer.write(self._LABELY)
        buffer.write(' labelZ=\"\"')
        buffer.write(self._UNITX)
        buffer.write(self._UNITY)
        buffer.write(self._XPRECISION)
        buffer.write(self._YPRECISION)
        buffer.write(self._STYLE)
        buffer.write(self._COLOR)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write('\t\t\t<input axis=\"x\">')
        buffer.write(self._INPUTX)
        buffer.write('</input>\n\t\t\t<input axis=\"y\">')
        buffer.write(self._INPUTY)
        buffer.write('</input>\n\t\t</graph>\n')

    class Edit(Element):
      def __init__(self):
        super().__init__()
        self._UNIT          = ""
        self._SIGNED        = ""
        self._DECIMAL       = ""
        self._XMLATTRIBUTE  = ""
        self._CHANNEL       = "CB1"

       
      @property
      def UNIT(self):
        return self._UNIT
        
      def SIGNED(self):
        return self._SIGNED
        
      def DECIMAL(self):
        return self._DECIMAL
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
    
      def CHANNEL(self):
        return self._CHANNEL
        
      def setUnit(self, strInput):
        self._ERROR = self.err_check_length(strInput,12,'setUnit') if self._ERROR._MESSAGE is "" else self._ERROR
        self._UNIT = " unit=\"" + strInput + "\""
        
      def setSigned(self, boolInput):
        if boolInput:
          self._SIGNED = " signed=\"true\""
        else:
          self._SIGNED = " signed=\"false\""
          
      def setDecimal(self, boolInput):
        if boolInput:
          self._DECIMAL = " decimal=\"true\""
        else:
          self._DECIMAL = " decimal=\"false\""
    
      def setXMLAttribute(self, strInput):
        self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XMLATTRIBUTE = " " + strInput
        
      def setChannel(self, intInput):
        self._ERROR = self.err_check_upper(intInput,1,'setChannel') if self._ERROR._MESSAGE is "" else self._ERROR
        self._CHANNEL = "CB" + str(intInput)

      def getBytes(self, buffer):
        buffer.write('\t\t<edit')
        buffer.write(self._LABEL)
        buffer.write(self._SIGNED)
        buffer.write(self._DECIMAL)
        buffer.write(self._UNIT)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write('\t\t\t<output>')
        buffer.write(self._CHANNEL)
        buffer.write('</output>\n')
        buffer.write('\t\t</edit>\n')
        
    class InfoField(Element):
      def __init__(self):
        super().__init__()
        self._INFO          = ""
        self._COLOR         = ""
        self._XMLATTRIBUTE  = ""
       
      @property
      def INFO(self):
        return self._INFO
        
      def COLOR(self):
        return self._COLOR
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
        
      def setInfo(self, strInput):
        self._ERROR = self.err_check_length(strInput,191,'setInfo') if self._ERROR._MESSAGE is "" else self._ERROR
        self._INFO = " label=\"" + strInput + "\""
        
      def setColor(self, strInput):
        self._ERROR = self.err_check_hex(strInput,'setColor') if self._ERROR._MESSAGE is "" else self._ERROR
        self._COLOR = " color=\"" + strInput + "\""
    
      def setXMLAttribute(self, strInput):
        self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XMLATTRIBUTE = " " + strInput

      def getBytes(self, buffer):
        buffer.write('\t\t<info')
        buffer.write(self._INFO)
        buffer.write(self._COLOR)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write('\t\t</info>\n')
        
    class Separator(Element):
      def __init__(self):
        super().__init__()
        self._HEIGHT        = ""
        self._COLOR         = ""
        self._XMLATTRIBUTE  = ""
       
      @property
      def INFO(self):
        return self._HEIGHT
        
      def COLOR(self):
        return self._COLOR
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
        
      def setHeight(self, fltInput):
        self._ERROR = self.err_check_length(str(fltInput),10,'setHeight') if self._ERROR._MESSAGE is "" else self._ERROR
        self._HEIGHT = " height=\"" + str(fltInput) + "\""
        
      def setColor(self, strInput):
        self._ERROR = self.err_check_hex(strInput,'setColor') if self._ERROR._MESSAGE is "" else self._ERROR
        self._COLOR = " color=\"" + strInput + "\""
    
      def setXMLAttribute(self, strInput):
        self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XMLATTRIBUTE = " " + strInput

      def getBytes(self, buffer):
        buffer.write('\t\t<separator')
        buffer.write(self._HEIGHT)
        buffer.write(self._COLOR)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write('\t\t</separator>\n')
        
    class Value(Element):
      def __init__(self):
        super().__init__()
        self._PRECISION     = ""
        self._UNIT          = ""
        self._COLOR         = ""
        self._XMLATTRIBUTE  = ""
        self._INPUTVALUE    = "CH3"
       
      @property
      def PRECISION(self):
        return self._PRECISION
    
      def UNIT(self):
        return self._UNIT
        
      def COLOR(self):
        return self._COLOR
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
    
      def INPUTVALUE(self):
        return self._INPUTVALUE
        
      def setPrecision(self, intInput):
        self._ERROR = self.err_check_upper(intInput,999,'setXPrecision') if self._ERROR._MESSAGE is "" else self._ERROR
        self._PRECISION = " precision=\"" + str(intInput) + "\""
        
      def setUnit(self, strInput):
        self._ERROR = self.err_check_length(strInput,12,'setUnit') if self._ERROR._MESSAGE is "" else self._ERROR
        self._UNIT = " unit=\"" + strInput + "\""
        
      def setColor(self, strInput):
        self._ERROR = self.err_check_hex(strInput,'setColor') if self._ERROR._MESSAGE is "" else self._ERROR
        self._COLOR = " color=\"" + strInput + "\""
    
      def setXMLAttribute(self, strInput):
        self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
        self._XMLATTRIBUTE = " " + strInput
        
      def setChannel(self, intInput):
        self._ERROR = self.err_check_upper(intInput,5,'setChannel') if self._ERROR._MESSAGE is "" else self._ERROR
        self._INPUTVALUE = "CH" + str(intInput)

      def getBytes(self, buffer):
        buffer.write('\t\t<value')
        buffer.write(self._LABEL)
        buffer.write(self._PRECISION)
        buffer.write(self._UNIT)
        buffer.write(' facor=\"1\"')
        buffer.write(self._COLOR)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write(' \t\t\t<input>')
        buffer.write(self._INPUTVALUE)
        buffer.write('</input>\n\t\t</value>\n')
        
    class ExportData(Element):
        def __init__(self):
            super().__init__()
            self._BUFFER        = "CH1"
            self._XMLATTRIBUTE  = ""
            self._LABEL = "data"
        
        def setLabel(self, strInput):
            self._ERROR = self.err_check_length(strInput,41,'setLabel') if self._ERROR._MESSAGE is "" else self._ERROR
            self._LABEL = " name=\"" + strInput + "\""
        
        def setDatachannel(self, intInput):
            self._ERROR = self.err_check_upper(intInput,5,'setChannel') if self._ERROR._MESSAGE is "" else self._ERROR
            self._BUFFER = "CH" + str(intInput)
        
        def setXMLAttribute(self, strInput):
            self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
            self._XMLATTRIBUTE = " " + strInput
            
        def getBytes(self, buffer):
            buffer.write('\t\t<data')
            buffer.write(self._LABEL)
            buffer.write(self._XMLATTRIBUTE)
            buffer.write('>')
            buffer.write(self._BUFFER)
            buffer.write('</data>\n')
            
    class ExportSet(Errorhandler):
        def __init__(self):
            super().__init__()
            self._LABEL         = ""
            self._XMLATTRIBUTE  = ""
            self._ERROR         = PhyphoxBleExperiment.Error()
            self._ELEMENTS      = [0]*phyphoxBleNExportSets
            
        def setLabel(self, strInput):
            self._ERROR = self.err_check_length(strInput,41,'setLabel') if self._ERROR._MESSAGE is "" else self._ERROR
            self._LABEL = " name=\"" + strInput + "\""
            
        def addElement(self, e):
            for i in range(phyphoxBleNExportSets):
                if not self._ELEMENTS[i]:
                    self._ELEMENTS[i] = e
                    break
                
        def setXMLAttribute(self, strInput):
            self._ERROR = self.err_check_length(strInput,98,'setXMLAttribute') if self._ERROR._MESSAGE is "" else self._ERROR
            self._XMLATTRIBUTE = " " + strInput
            
        def getBytes(self, buffer):
            buffer.write('\t<set')
            buffer.write(self._LABEL)
            buffer.write(self._XMLATTRIBUTE)
            buffer.write('>\n')
            for i in range(phyphoxBleNExportSets):
                if self._ELEMENTS[i]:
                    self._ELEMENTS[i].getBytes(buffer)
            buffer.write('\t</set>\n')
