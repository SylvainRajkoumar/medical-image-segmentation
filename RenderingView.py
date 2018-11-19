import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt


class RenderingView(QFrame):

    def __init__(self):
        QFrame.__init__(self)
        self.vtk_image_reader = vtk.vtkDICOMImageReader()
        self.window_initialization()

    def load_dicom(self, directory):

        self.vtk_image_reader.SetDirectoryName(directory)
        self.vtk_image_reader.Update()
        self.update_rendering_view()

    def window_initialization(self):
        vertical_layout = QVBoxLayout()
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.vtk_widget.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        vertical_layout.addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.renderer.ResetCamera()
        self.renderer.SetBackground(0,0,0)

        self.setLayout(vertical_layout)
        self.renderer_interactor.Initialize()

    def update_rendering_view(self):
        self.renderer.Clear()
        self.renderer.ResetCamera()
        self.renderer.SetBackground(0,0,0)

        arterExtractor = vtk.vtkContourFilter()
        arterExtractor.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        arterExtractor.SetValue(0, 350)
        arterNormals = vtk.vtkPolyDataNormals() #Passage de la matrice de pixels à des coordonées géométriques / 3D
        arterNormals.SetInputConnection(arterExtractor.GetOutputPort())
        arterNormals.SetFeatureAngle(100.0)
        arterStripper = vtk.vtkStripper() #Génération d'un ensemble de polygone à partir des coordonées calculées précédemment
        arterStripper.SetInputConnection(arterNormals.GetOutputPort())
        arterMapper = vtk.vtkPolyDataMapper() #Permet de passer des polygones à des formes géométriques graphiques
        arterMapper.SetInputConnection(arterStripper.GetOutputPort())
        arterMapper.ScalarVisibilityOff()
        
        arter = vtk.vtkActor()
        arter.SetMapper(arterMapper)
        arter.GetProperty().SetDiffuseColor(1, 1, .9412)
        
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        outline = vtk.vtkActor()
        outline.SetMapper(mapOutline)
        outline.GetProperty().SetColor(1,1,1)

        self.renderer.AddActor(outline)
        self.renderer.AddActor(arter)

        self.renderer_interactor.Initialize()