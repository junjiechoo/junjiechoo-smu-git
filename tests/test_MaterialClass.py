from sqlalchemy.sql.expression import null
import pytest
from app.models.database import *
from .conftest import *

# Done by Low Jun Yi
def test_get_materialId(material):
    assert material.getMaterialId() == "M001"
    
def test_get_materialName(material):
    assert material.getMaterialName() == "link"

def test_get_materialType(material):
    assert material.getMaterialType() == "hyperlink"

def test_get_fileLink(material):
    assert material.getFileLink() == "https://www.github.com/"
    
def test_set_materialId(material):
    material.setMaterialId("M002")
    assert material.getMaterialId() == "M002"
    
def test_set_materialName(material):
    material.setMaterialName("link 2")
    assert material.getMaterialName() == "link 2"

def test_set_materialType(material):
    material.setMaterialType("hyperlink")
    assert material.getMaterialType() == "hyperlink"

def test_set_fileLink(material):
    material.setFileLink("https://www.youtube.com/")
    assert material.getFileLink() == "https://www.youtube.com/"