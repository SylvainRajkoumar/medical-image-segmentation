import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from utils.decorators import timeit

filename = "extracted.stl"
stl_writer = vtk.vtkSTLWriter()
stl_writer.SetFileName(filename)

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

    def reset(self):
        self.vtk_image_reader = vtk.vtkDICOMImageReader()
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
        self.renderer.SetBackground(0.1, 0.1, 0.2)
        self.arterExtractor = vtk.vtkContourFilter()
        self.arterExtractor.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        self.arterExtractor.SetValue(0, self.rendering_threshold)

        self.arterNormals = vtk.vtkPolyDataNormals()
        self.arterNormals.SetInputConnection(self.arterExtractor.GetOutputPort())
        self.arterNormals.SetFeatureAngle(100.0)

        stl_writer.SetInputConnection(self.arterNormals.GetOutputPort())
        stl_writer.Write()
        
        self.arterStripper = vtk.vtkStripper()
        self.arterStripper.SetInputConnection(self.arterNormals.GetOutputPort())

        self.arterMapper = vtk.vtkPolyDataMapper()
        self.arterMapper.SetInputConnection(self.arterStripper.GetOutputPort())
        self.arterMapper.ScalarVisibilityOff()
        
        self.arter.SetMapper(self.arterMapper)
        self.arter.GetProperty().SetDiffuseColor(1, 1, .9412)
        
        self.outlineData = vtk.vtkOutlineFilter()
        self.outlineData.SetInputConnection(self.vtk_image_reader.GetOutputPort())
        self.mapOutline = vtk.vtkPolyDataMapper()
        self.mapOutline.SetInputConnection(self.outlineData.GetOutputPort())

        self.outline.SetMapper(self.mapOutline)
        self.outline.GetProperty().SetColor(1, 1, 1)

        self.renderer.AddActor(self.outline)
        self.renderer.AddActor(self.arter)
   
        self.renderer.ResetCamera()
        self.renderer_interactor.Initialize()

    # def save_stl(self):
    #     stl_writer.SetInputConnection(self.arterNormals.GetOutputPort())
    #     stl_writer.Write()