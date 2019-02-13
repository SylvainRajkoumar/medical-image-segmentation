import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from utils.decorators import timeit

filename = "test.stl"
stlWriter = vtk.vtkSTLWriter()
stlWriter.SetFileName(filename)


class RenderingView(QFrame):

    def __init__(self):
        QFrame.__init__(self)
        self.rendering_threshold = 0
        self.arter = vtk.vtkActor()
        self.outline = vtk.vtkActor()
        self.vtk_image_reader = vtk.vtkDICOMImageReader()
        self.window_initialization()

    def set_rendering_threshold(self, value):
        self.rendering_threshold = value

    @timeit
    def load_dicom(self, directory):
        self.vtk_image_reader = vtk.vtkDICOMImageReader()
        self.vtk_image_reader.SetDirectoryName(directory)
        self.vtk_image_reader.Update()
        self.update_rendering_view()

    @timeit
    def window_initialization(self):
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0,0,0,0)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.vtk_widget.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        vertical_layout.addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.renderer.SetBackground(0,0,0)

        self.setLayout(vertical_layout)
        self.renderer_interactor.Initialize()
    
    def reset_camera(self):
        self.renderer.ResetCamera()
        self.renderer_interactor.Initialize()

    @timeit
    def update_rendering_view(self, *args):
        self.renderer.RemoveActor(self.outline)
        self.renderer.RemoveActor(self.arter)

        self.arterExtractor = vtk.vtkContourFilter()
        self.arterExtractor.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        self.arterExtractor.SetValue(0, self.rendering_threshold)

        arterNormals = vtk.vtkPolyDataNormals() #Calcul des normales
        arterNormals.SetInputConnection(self.arterExtractor.GetOutputPort())
        arterNormals.SetFeatureAngle(100.0)
        stlWriter.SetInputConnection(arterNormals.GetOutputPort())
        stlWriter.Write()

        arterStripper = vtk.vtkStripper() #Génération d'un ensemble de polygone à partir des coordonées calculées précédemment
        arterStripper.SetInputConnection(arterNormals.GetOutputPort())

        arterMapper = vtk.vtkPolyDataMapper() #Permet de passer des polygones à des formes géométriques graphiques
        arterMapper.SetInputConnection(arterStripper.GetOutputPort())
        arterMapper.ScalarVisibilityOff()
        
        self.arter.SetMapper(arterMapper)
        self.arter.GetProperty().SetDiffuseColor(1, 1, .9412)
        
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        self.outline.SetMapper(mapOutline)
        self.outline.GetProperty().SetColor(1, 1, 1)

        self.renderer.AddActor(self.outline)
        self.renderer.AddActor(self.arter)
   
        self.renderer.ResetCamera()
        self.renderer_interactor.Initialize()