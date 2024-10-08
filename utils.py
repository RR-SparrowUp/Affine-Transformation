import numpy as np
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import cv2

# ==============================
# Define Plotting Functions First
# ==============================

def plot_skeleton(kps_2d, ax=None, title=None, show=True, save_path=None, invert_y=False):
    """
    Plots a 2D skeleton based on provided keypoints.

    Parameters:
    - kps_2d (dict): A dictionary of keypoints with their (x, y) coordinates.
    - ax (matplotlib.axes.Axes, optional): An existing Axes object to plot on.
    - title (str, optional): Title of the plot.
    - show (bool, optional): Whether to display the plot immediately.
    - save_path (str, optional): File path to save the plot image. If None, the image won't be saved.
    - invert_y (bool, optional): Whether to invert the Y-axis.

    Returns:
    - ax (matplotlib.axes.Axes): The Axes object with the plot.
    """
    # Define the skeletal connections
    skeleton_connections = [
        ('Head', 'Neck'),
        ('Neck', 'Chest'),
        ('Chest', 'Hips'),
        ('Neck', 'LeftShoulder'),
        ('LeftShoulder', 'LeftArm'),
        ('LeftArm', 'LeftForearm'),
        ('LeftForearm', 'LeftHand'),
        ('Chest', 'RightShoulder'),
        ('RightShoulder', 'RightArm'),
        ('RightArm', 'RightForearm'),
        ('RightForearm', 'RightHand'),
        ('Hips', 'LeftThigh'),
        ('LeftThigh', 'LeftLeg'),
        ('LeftLeg', 'LeftFoot'),
        ('Hips', 'RightThigh'),
        ('RightThigh', 'RightLeg'),
        ('RightLeg', 'RightFoot'),
        ('RightHand', 'RightFinger'),
        ('RightFinger', 'RightFingerEnd'),
        ('LeftHand', 'LeftFinger'),
        ('LeftFinger', 'LeftFingerEnd'),
        ('Head', 'HeadEnd'),
        ('RightFoot', 'RightHeel'),
        ('RightHeel', 'RightToe'),
        ('RightToe', 'RightToeEnd'),
        ('LeftFoot', 'LeftHeel'),
        ('LeftHeel', 'LeftToe'),
        ('LeftToe', 'LeftToeEnd')
    ]
    
    # Create a new figure and axes if none are provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        fig = ax.figure

    # Filter out any non-keypoint entries
    keypoints = {k: v for k, v in kps_2d.items() if isinstance(v, list) and len(v) == 2}

    # Plot keypoints
    for key, (x, y) in keypoints.items():
        ax.scatter(x, y, color='red', zorder=5)
        # Uncomment the next line to label keypoints
        # ax.text(x + 5, y + 5, key, fontsize=8, zorder=10)

    # Plot skeletal connections
    for joint1, joint2 in skeleton_connections:
        if joint1 in keypoints and joint2 in keypoints:
            x_values = [keypoints[joint1][0], keypoints[joint2][0]]
            y_values = [keypoints[joint1][1], keypoints[joint2][1]]
            ax.plot(x_values, y_values, 'b-', linewidth=2, zorder=1)

    # Customize the plot
    if title:
        ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')
    if invert_y:
        ax.invert_yaxis()  # Invert Y-axis if required
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    # Save the plot if save_path is provided
    if save_path:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            fig.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
            print(f"Plot saved successfully at: {save_path}")
        except Exception as e:
            print(f"Error saving plot: {e}")

    if show:
        plt.show()
    
    return ax

def plot_skeleton_custom(kps_2d, ax=None, title=None, show=True, save_path=None, color='red', marker='o', invert_y=False):
    """
    Custom plot_skeleton function to allow color and marker customization.

    Parameters:
    - kps_2d (dict): A dictionary of keypoints with their (x, y) coordinates.
    - ax (matplotlib.axes.Axes, optional): An existing Axes object to plot on.
    - title (str, optional): Title of the plot.
    - show (bool, optional): Whether to display the plot immediately.
    - save_path (str, optional): File path to save the plot image. If None, the image won't be saved.
    - color (str or tuple): Color of the skeleton.
    - marker (str): Marker style for keypoints.
    - invert_y (bool, optional): Whether to invert the Y-axis.

    Returns:
    - ax (matplotlib.axes.Axes): The Axes object with the plot.
    """
    # Define the skeletal connections (same as above)
    skeleton_connections = [
        ('Head', 'Neck'),
        ('Neck', 'Chest'),
        ('Chest', 'Hips'),
        ('Neck', 'LeftShoulder'),
        ('LeftShoulder', 'LeftArm'),
        ('LeftArm', 'LeftForearm'),
        ('LeftForearm', 'LeftHand'),
        ('Chest', 'RightShoulder'),
        ('RightShoulder', 'RightArm'),
        ('RightArm', 'RightForearm'),
        ('RightForearm', 'RightHand'),
        ('Hips', 'LeftThigh'),
        ('LeftThigh', 'LeftLeg'),
        ('LeftLeg', 'LeftFoot'),
        ('Hips', 'RightThigh'),
        ('RightThigh', 'RightLeg'),
        ('RightLeg', 'RightFoot'),
        ('RightHand', 'RightFinger'),
        ('RightFinger', 'RightFingerEnd'),
        ('LeftHand', 'LeftFinger'),
        ('LeftFinger', 'LeftFingerEnd'),
        ('Head', 'HeadEnd'),
        ('RightFoot', 'RightHeel'),
        ('RightHeel', 'RightToe'),
        ('RightToe', 'RightToeEnd'),
        ('LeftFoot', 'LeftHeel'),
        ('LeftHeel', 'LeftToe'),
        ('LeftToe', 'LeftToeEnd')
    ]
    
    # Create a new figure and axes if none are provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        fig = ax.figure

    # Filter out any non-keypoint entries
    keypoints = {k: v for k, v in kps_2d.items() if isinstance(v, list) and len(v) == 2}

    # Plot keypoints
    for key, (x, y) in keypoints.items():
        ax.scatter(x, y, color=color, zorder=5, marker=marker)
        # Uncomment the next line to label keypoints
        # ax.text(x + 5, y + 5, key, fontsize=8, zorder=10)

    # Plot skeletal connections
    for joint1, joint2 in skeleton_connections:
        if joint1 in keypoints and joint2 in keypoints:
            x_values = [keypoints[joint1][0], keypoints[joint2][0]]
            y_values = [keypoints[joint1][1], keypoints[joint2][1]]
            ax.plot(x_values, y_values, color=color, linewidth=2, zorder=1)

    # Customize the plot
    if title:
        ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')
    if invert_y:
        ax.invert_yaxis()  # Invert Y-axis if required
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    # Save the plot if save_path is provided
    if save_path:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            fig.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
            print(f"Plot saved successfully at: {save_path}")
        except Exception as e:
            print(f"Error saving plot: {e}")

    if show:
        plt.show()
    
    return ax
