from datetime import datetime
from pathlib import Path
import shutil


PROJECT_ROOT = Path(__file__).resolve().parent.parent

ROUTINE_FILE = PROJECT_ROOT / "nushluxe_data_v2.json"
PRODUCT_FILE = PROJECT_ROOT / "nushluxe_products.json"

BACKUP_FOLDER = PROJECT_ROOT / "backups"


def create_backup():

    BACKUP_FOLDER.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    routine_backup = (
        BACKUP_FOLDER
        / f"nushluxe_data_v2_{timestamp}.json"
    )

    product_backup = (
        BACKUP_FOLDER
        / f"nushluxe_products_{timestamp}.json"
    )

    shutil.copy2(
        ROUTINE_FILE,
        routine_backup
    )

    shutil.copy2(
        PRODUCT_FILE,
        product_backup
    )

    print("Nushluxe backup created.")
    print()
    print(
        f"Routine backup: {routine_backup.name}"
    )
    print(
        f"Product backup: {product_backup.name}"
    )
    print()
    print(
        f"Backup folder: {BACKUP_FOLDER}"
    )


if __name__ == "__main__":
    create_backup()