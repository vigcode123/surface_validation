# Import necessary libraries
import trimesh
import matplotlib.pyplot as plt
import configparser
import math
import numpy as np
from pathlib import Path
from tqdm import tqdm
import ast

# Read configuration from ini file
config = configparser.ConfigParser()
config.read("mesh.ini")

# Set the target directory for STL files
target_dir = Path(config["DEFAULT"]["PathToSTLFiles"])
if not target_dir.exists():
    raise RuntimeError("The target directory doesn't exist")

# Get list of valid STL files in the target directory
filelst = [x.name for x in list(target_dir.iterdir()) if x.name.split(".")[1] in ast.literal_eval(config["DEFAULT"]["ValidatedFileEndings"])]

# Perform checks on each file
if (len(filelst) <= int(config["DEFAULT"]["MaximumFilesForVerbosity"])):
    for file in filelst:
        mesh = trimesh.load(config["DEFAULT"]["PathToSTLFiles"] + file)
        print("Starting with "+file)
        
        # Check 1: Verify if volume is defined and positive
        print("Check 1: Checking if volume is defined and positive ...")
        if (mesh.is_empty or mesh.volume == 0):
            raise RuntimeError("no data is on the current mesh")
        print("Check 1 completed.\n---------------------------")
        
        # Check 2: Verify if edges are manifold
        print("Check 2: Checking if edges are manifold ...")
        edge_manifold_check = [0]*mesh.faces.shape[0]
        for adj in mesh.face_adjacency:
            edge_manifold_check[adj[0]]+=1
            edge_manifold_check[adj[1]]+=1
        
        for check2 in range(len(edge_manifold_check)):
            if edge_manifold_check[check2] != 3:
                mesh.visual.face_colors[check2] = np.array([255,0,0,255])
                mesh.show()
                raise RuntimeError("Edge not manifold on face "+str(mesh.faces[check2])+" at index "+str(check2))
        print("Check 2 completed.\n---------------------------")
        
        # Check 2.5: Verify if vertices are manifold
        print("Check 2.5: Checking if vertices are manifold ...")
        for vd in range(len(mesh.vertex_degree)):
            if mesh.vertex_degree[vd] < 3:
                mesh.visual.vertex_colors[vd] = np.array([255,0,0,255])
                mesh.show()
                raise RuntimeError("Vertex not manifold on at index "+str(mesh.vertices[vd]))
        print("Check 2.5 completed.\n---------------------------")
        
        # Check 3: Verify if shape is watertight (no holes)
        print("Check 3: Checking if shape is watertight (no holes)")
        if not mesh.is_watertight:
            print("Holes detected. Attempting to fix.")
            mesh.fill_holes()
            mesh.fix_normals()
            trimesh.repair.broken_faces(mesh, color=[255,0,0,255])
            if not mesh.is_watertight:
                mesh.show()
                raise RuntimeError("Holes detected. Unable to fix")
            print("Holes fixed.")
        print("Check 3 completed.\n---------------------------")
        
        # Check 4: Verify triangle angles (optional)
        if "y" in config["DEFAULT"]["IncludeCheckFour"].lower():
            print("Check 4: Checking too thin triangles ...")
            for angles in range(len(mesh.face_angles)):
                for a in range(len(mesh.face_angles[angles])):
                    if mesh.face_angles[angles][a] < math.radians(int(config["DEFAULT"]["ThreshForTriAngle"])):
                        mesh.visual.face_colors[angles]  = np.array([255,0,0,255])
                        mesh.show()
                        raise RuntimeError("Angle #"+str(a+1)+" on face #"+str(angles+1)+" too small, rendering too thin("+str(math.degrees(mesh.face_angles[angles][a]))+") to be useful.")
            print("Check 4 completed.\n---------------------------")
        
        # Check 5: Verify for abnormal sharp points (optional)
        if "y" in config["DEFAULT"]["IncludeCheckFive"].lower():
            print("Check 5: Checking for abnormal sharp points")
            sharp_vertices = [mesh.vertices[np.where(mesh.vertex_defects == x)[0][0]] for x in mesh.vertex_defects if abs(x) < int(config["DEFAULT"]["ThreshForAngleDefect"])]
            if len(sharp_vertices) > 0:
                raise RuntimeError("Sharp jutting detected at these vertices: "+str(sharp_vertices))
            print("Check 5 completed.\n---------------------------")
        
        # Check 6: Verify winding consistency (optional)
        if "y" in config["DEFAULT"]["IncludeConsistentWinding"].lower():
            print("Check 6: Checking if winding consistent")
            if not mesh.is_winding_consistent:
                raise RuntimeError("Winding not consistent in this mesh. Change the configuration if you do not want to check for this.")
            print("Check 6 completed.\n---------------------------")
        
        print(file+ " all good")
else:
    # If there are many files, use a progress bar
    for file in tqdm(filelst):
        mesh = trimesh.load(config["DEFAULT"]["PathToSTLFiles"] + file)
        
        # Perform the same checks as above, but with less verbose output
        if (mesh.is_empty or mesh.volume == 0):
            raise RuntimeError("no data is on the current mesh for "+file)
        
        edge_manifold_check = [0]*mesh.faces.shape[0]
        for adj in mesh.face_adjacency:
            edge_manifold_check[adj[0]]+=1
            edge_manifold_check[adj[1]]+=1
        
        for check2 in range(len(edge_manifold_check)):
            if edge_manifold_check[check2] != 3:
                mesh.visual.face_colors[check2] = np.array([255,0,0,255])
                mesh.show()
                raise RuntimeError("Edge not manifold on face "+str(mesh.faces[check2])+" at index "+str(check2)+"for "+file)
        
        print(mesh.vertex_degree)
        for vd in range(len(mesh.vertex_degree)):
            if mesh.vertex_degree[vd] <3:
                mesh.visual.vertex_colors[vd] = np.array([255,0,0,255])
                mesh.show()
                raise RuntimeError("Vertex not manifold on at index "+str(mesh.vertices[vd])+" in "+file)
        
        if not mesh.is_watertight:
            mesh.fill_holes()
            mesh.fix_normals()
            trimesh.repair.broken_faces(mesh, color=[255,0,0,255])
            if not mesh.is_watertight:
                mesh.show()
                raise RuntimeError("Holes detected. Unable to fix in "+file)
        
        if "y" in config["DEFAULT"]["IncludeCheckFour"].lower():
            for angles in range(len(mesh.face_angles)):
                for a in range(len(mesh.face_angles[angles])):
                    if mesh.face_angles[angles][a] < math.radians(int(config["DEFAULT"]["ThreshForTriAngle"])):
                        mesh.visual.face_colors[angles]  = np.array([255,0,0,255])
                        mesh.show()
                        raise RuntimeError("Angle #"+str(a+1)+" on face #"+str(angles+1)+" too small, rendering too thin("+str(math.degrees(mesh.face_angles[angles][a]))+") to be useful. Found in "+file)
        
        if "y" in config["DEFAULT"]["IncludeCheckFive"].lower():
            sharp_vertices = [mesh.vertices[np.where(mesh.vertex_defects == x)[0][0]] for x in mesh.vertex_defects if abs(x) < int(config["DEFAULT"]["ThreshForAngleDefect"])]
            if len(sharp_vertices) > 0:
                raise RuntimeError("Sharp jutting detected at these vertices: "+str(sharp_vertices)+". Found in "+file)
        
        if "y" in config["DEFAULT"]["IncludeConsistentWinding"].lower():
            if not mesh.is_winding_consistent:
                raise RuntimeError("Winding not consistent in this mesh. Change the configuration if you do not want to check for this.")