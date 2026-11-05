from pathlib import Path
import shutil


def get_sample_files():
    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

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

    return (
        sample_routines,
        sample_products
    )


def ensure_local_data_files(
    routine_data_file,
    product_data_file
):

    (
        sample_routines,
        sample_products
    ) = get_sample_files()

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


def reset_demo_data_files(
    routine_data_file,
    product_data_file
):

    (
        sample_routines,
        sample_products
    ) = get_sample_files()

    routine_data_file = Path(
        routine_data_file
    )

    product_data_file = Path(
        product_data_file
    )

    routine_data_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    product_data_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(
        sample_routines,
        routine_data_file
    )

    shutil.copy2(
        sample_products,
        product_data_file
    )