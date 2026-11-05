from pathlib import Path
import shutil


def ensure_local_data_files(
    routine_data_file,
    product_data_file
):

    project_root = Path(
        __file__
    ).resolve().parent.parent

    sample_folder = (
        project_root / "sample_data"
    )

    sample_routines = (
        sample_folder
        / "sample_routines.json"
    )

    sample_products = (
        sample_folder
        / "sample_products.json"
    )

    routine_data_file = Path(
        routine_data_file
    )

    product_data_file = Path(
        product_data_file
    )

    if not routine_data_file.exists():

        shutil.copy2(
            sample_routines,
            routine_data_file
        )

    if not product_data_file.exists():

        shutil.copy2(
            sample_products,
            product_data_file
        )