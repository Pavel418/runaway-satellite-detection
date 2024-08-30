import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths
base_dir = r'C:\Users\Pavel\Documents\GitHub\runaway-satellite-detection\multiple_roads'

# Define target directories
# These are the directories where a subdirectory should be created before moving files
target_dirs_with_subdirs = [r'C:\Users\Pavel\Documents\Github\runaway-satellite-detection\bad-multi', r'C:\Users\Pavel\Documents\Github\runaway-satellite-detection\good-multi']#[r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\bad_quality_data', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\cloud_covered_data', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\inactive_roads', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\perfect_data', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\normal_data', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\relabel']

# These are the directories where files should be moved directly
target_dirs_direct_move = []#[r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\negative_samples\clouds', r'C:\Users\Admin\Documents\GitHub\runaway-satellite-detection\negative_samples\no_road']

# Combine the lists for selection purposes
target_dirs = target_dirs_with_subdirs + target_dirs_direct_move

# Add an option to delete the directory
delete_option_index = len(target_dirs)
target_dirs.append('Delete the directory')

# Iterate over the main subdirectories
for sub_dir_name in os.listdir(base_dir):
    sub_dir = os.path.join(base_dir, sub_dir_name)
    for sub_sub_dir in os.listdir(sub_dir):
        sub_sub_dir_path = os.path.join(sub_dir, sub_sub_dir)
        
        # Get the PNG file
        png_file = [f for f in os.listdir(sub_sub_dir_path) if f.endswith('.png')][0]
        png_path = os.path.join(sub_sub_dir_path, png_file)
        
        # Display the image
        plt.figure(figsize=(150, 150))
        img = mpimg.imread(png_path)
        plt.imshow(img)
        plt.axis('off')
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()
        
        # Display the target directories with corresponding numbers, including the delete option
        print("\nSelect the target directory or choose to delete:")
        for idx, target_dir in enumerate(target_dirs):
            if idx == delete_option_index:
                print(f"{idx}: Delete the directory")
            else:
                print(f"{idx}: {os.path.basename(target_dir)}")

        # Get user input
        selection = int(input("Enter a number from 0 to 8 to move the directory: "))
        
        # Handle deletion or move operation
        if selection == delete_option_index:
            shutil.rmtree(sub_sub_dir_path)
            print(f"Deleted {sub_sub_dir_path}")
        else:
            # Determine the target directory
            target_dir = target_dirs[selection]

            # Check if the selected directory is in the list that requires subdirectory creation
            if target_dir in target_dirs_with_subdirs:
                final_target_dir = os.path.join(target_dir, sub_dir_name)
                # Create the target subdirectory if it doesn't exist
                if not os.path.exists(final_target_dir):
                    print(f"Creating subdirectory {final_target_dir}")  
                    os.makedirs(final_target_dir)
                else:
                    print(f"Subdirectory {final_target_dir} already exists")
                # Move the directory
                shutil.move(sub_sub_dir_path, final_target_dir)
                print(f"Moved {sub_sub_dir_path} to {final_target_dir}")
            else:
                new_name = os.path.join(sub_dir, f'{os.path.basename(sub_dir)}_{sub_sub_dir}')
                os.rename(sub_sub_dir_path, new_name)
                final_target_dir = target_dir
                shutil.move(new_name, final_target_dir)
                print(f"Moved {new_name} to {final_target_dir}")
