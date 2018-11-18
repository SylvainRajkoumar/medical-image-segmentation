# self.verticalLayout = QVBoxLayout()
# self.vtkWidget = QVTKRenderWindowInteractor(self)
# self.vtkWidget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
# self.verticalLayout.addWidget(self.vtkWidget)
# self.renderer = vtk.vtkRenderer()
# self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
# self.rendererInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
# self.renderer.ResetCamera()
# self.renderer.SetBackground(0,0,0)

# self.vtkImageReader = vtk.vtkDICOMImageReader()
# self.vtkImageReader.SetDirectoryName("D:/Projet_3CT/Data_IRM/05-JR")
# self.vtkImageReader.Update()

# arterExtractor = vtk.vtkContourFilter()
# arterExtractor.SetInputConnection(self.vtkImageReader.GetOutputPort())
# arterExtractor.SetValue(0, 350)
# arterNormals = vtk.vtkPolyDataNormals() #Passage de la matrice de pixels à des coordonées géométriques / 3D
# arterNormals.SetInputConnection(arterExtractor.GetOutputPort())
# arterNormals.SetFeatureAngle(100.0)
# arterStripper = vtk.vtkStripper() #Génération d'un ensemble de polygone à partir des coordonées calculées précédemment
# arterStripper.SetInputConnection(arterNormals.GetOutputPort())
# arterMapper = vtk.vtkPolyDataMapper() #Permet de passer des polygones à des formes géométriques graphiques
# arterMapper.SetInputConnection(arterStripper.GetOutputPort())
# arterMapper.ScalarVisibilityOff()
# arter = vtk.vtkActor() #Objet dans un scène de rendu (comprends l'objet + éclairage + texture)
# arter.SetMapper(arterMapper)
# arter.GetProperty().SetDiffuseColor(1, 1, .9412)

# outlineData = vtk.vtkOutlineFilter()
# outlineData.SetInputConnection(self.vtkImageReader.GetOutputPort())
# mapOutline = vtk.vtkPolyDataMapper()
# mapOutline.SetInputConnection(outlineData.GetOutputPort())
# outline = vtk.vtkActor()
# outline.SetMapper(mapOutline)
# outline.GetProperty().SetColor(1,1,1)

# self.renderer.AddActor(outline)
# self.renderer.AddActor(arter)

# self.setLayout(self.verticalLayout)
# self.rendererInteractor.Initialize()