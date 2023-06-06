def collect(self):
        geomunits = self.unit_box.currentText()
        if geomunits == 'm':
            correct = 1
        elif geomunits == 'cm':
            correct = 0.01
        elif geomunits == 'mm':
            correct = 0.001
        tempunits = self.temp_box.currentText()
        if tempunits != 'K':
            tempcorrect = 0
        elif tempunits == 'K':
            tempcorrect = 273.15        
        #Collect data
        self.result = {}
        self.result['RG'] = [float(self.room['RL'].text())*correct, float(self.room['RW'].text())*correct, float(self.room['RH'].text())*correct]
        #Walls
        Uwall = []
        EPSwall = []
        Texwall = []
        #Walls OP 
        wallOpcoord = [[], [], [], []]
        EPSwallOp = [[], [], [], []]        
        UwallOp = [[], [], [], []]
        wallOpcoord_list = []
        #Walls RS
        EPSwallRS = [[],[],[],[]]
        TinwallRS = [[],[],[],[]]
        wallRScoord = [[],[],[],[]]
        wallRScoord_list = []
        #Floor and Ceiling RS
        RS_coord = {'Ceiling':[], 'Floor':[]}
        RS_coord_list = []
        RS_eps_cd = {'Ceiling':[], 'Floor':[]}
        RS_T_cd = {'Ceiling':[], 'Floor':[]}
        name_list = ['Ceiling', 'Floor']
        wall_name_list = ['Wall 1', 'Wall 2', 'Wall 3', 'Wall 4']
        for current_name in name_list:
            for RS_num in self.RS_data[current_name]:
                RS_coord_list.clear()
                RS_eps_cd[current_name].append(float(self.RS_eps[current_name][RS_num].text()))
                RS_T_cd[current_name].append(float(self.RS_T[current_name][RS_num].text()) - tempcorrect)
                RS_coord_list.append(float(self.RS_coord[current_name][RS_num]['x'].text()))
                RS_coord_list.append(float(self.RS_coord[current_name][RS_num]['W'].text()))
                RS_coord_list.append(float(self.RS_coord[current_name][RS_num]['y'].text()))
                RS_coord_list.append(float(self.RS_coord[current_name][RS_num]['L'].text()))
                RS_coord[current_name].append(RS_coord_list)


        for key in wall_name_list:
            wall_number = int(key[-1])-1
            Uwall.append(float(self.U[key].text()))
            EPSwall.append(float(self.eps[key].text()))
            Texwall.append(float(self.Tout[key].text()) - tempcorrect)
            for RS_num in self.RS_data[key]:
                wallRScoord_list.clear()
                EPSwallRS[wall_number].append(float(self.RS_eps[key][RS_num].text()))
                TinwallRS[wall_number].append(float(self.RS_T[key][RS_num].text()) - tempcorrect)
                wallRScoord_list.append(float(self.RS_coord[key][RS_num]['x'].text()))
                wallRScoord_list.append(float(self.RS_coord[key][RS_num]['W'].text()))
                wallRScoord_list.append(float(self.RS_coord[key][RS_num]['y'].text()))
                wallRScoord_list.append(float(self.RS_coord[key][RS_num]['L'].text()))
                wallRScoord[wall_number].append(wallRScoord_list)
            for door_num in self.door_data[key]:
                wallOpcoord_list.clear()
                EPSwallOp[wall_number].append(float(self.door_eps[key][door_num].text()))
                UwallOp[wall_number].append(float(self.door_U[key][door_num].text()))
                wallOpcoord_list.append(float(self.door_coord[key][door_num]['x'].text()))
                wallOpcoord_list.append(float(self.door_coord[key][door_num]['W'].text()))
                wallOpcoord_list.append(float(self.door_coord[key][door_num]['y'].text()))
                wallOpcoord_list.append(float(self.door_coord[key][door_num]['L'].text()))
                wallOpcoord[wall_number].append(wallOpcoord_list)


        self.result['Uwall'] = Uwall
        self.result['EPSwall'] = EPSwall
        self.result['Texwall'] = Texwall

        self.result['EPSwallRS'] = EPSwallRS
        self.result['TinwallRS'] = TinwallRS
        self.result['wallRScoord'] = wallRScoord

        self.result['EPSwallOp'] = EPSwallOp
        self.result['TexwallOp'] = Texwall
        self.result['UwallOp'] = UwallOp
        self.result['wallOpcoord'] = wallOpcoord
      
        self.result['Ufloor'] = float(self.U['Floor'].text())
        self.result['EPSfloor'] = float(self.eps['Floor'].text())
        self.result['Texfloor'] = float(self.Tout['Floor'].text()) - tempcorrect

        self.result['EPSfloorRS'] = RS_eps_cd['Floor']
        self.result['TfloorRS'] = RS_T_cd['Floor']
        self.result['floorRScoord'] = RS_coord['Floor']

        self.result['Uceiling'] = float(self.U['Ceiling'].text())
        self.result['EPSceiling'] = float(self.eps['Ceiling'].text())
        self.result['Texceiling'] = float(self.Tout['Ceiling'].text()) - tempcorrect

        self.result['EPSceilingRS'] = RS_eps_cd['Ceiling']
        self.result['TceilingRS'] = RS_T_cd['Ceiling']
        self.result['ceilingRScoord'] = RS_coord['Ceiling']

        name_list = ['Ceiling', 'Floor', 'Wall 1', 'Wall 2', 'Wall 3', 'Wall 4']
        geo_dict = {}

        for current_name in name_list:
            if self.water_switch[current_name] == True:

                geo = []
                table_name = self.water_table[current_name]
                for current_row in range(table_name.rowCount()):
                    layer_list = []
                    cap_mat_list = []
                    for col_num in range(1,4,1):
                        item = table_name.item(current_row, col_num).text()
                        if (col_num != 3):
                            layer_list.append(float(item))
                        elif (col_num == 3) and (item != ''):
                            cap_mat_list.append(float(self.mat_diam_box[current_name].currentText())/2 - 0.2) 
                            cap_mat_list.append(float(self.mat_diam_box[current_name].currentText())/2)
                            cap_mat_list.append(float(item))
                            cap_mat_list.append(0.22)
                            layer_list.append(cap_mat_list)
                    geo.append(layer_list)
                geo_dict[current_name] = [geo, float(self.mat_step_box[current_name].currentText()), float(self.RS_T[current_name][RS_num].text()) - tempcorrect]       

                            
        self.result['Water_calc'] = geo_dict       

        return(self.result)