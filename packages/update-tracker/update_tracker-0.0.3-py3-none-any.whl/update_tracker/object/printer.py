import click
from update_tracker.utils import Level, PackageData

class Printer():
    def __init__(self, summary, level) -> None:
        self.summary = summary
        self.level = level

    def make_output(self, result, error) -> None:
        self.print_package_report(result)
        if error:
            self.print_error(error)      
    
    def print_package_report(self, result) -> None:
        HEADER = """\n\n[REPORT]\n""" + "-" * 80
        FORMAT = "{:<20}" * (len(PackageData._fields) + 1)
        click.echo(HEADER)
        for level in Level:
            result_level = level.value - 1
            if result[result_level]:
                if not self.summary:
                    click.echo(f"**{level.name} 업데이트가 이미 진행된 패키지입니다!**")
                    click.echo(FORMAT.format('package_name', *PackageData._fields))
                    
                    for package_name, package_data in result[result_level].items():
                        click.echo(FORMAT.format(package_name, *package_data))

                else:
                    click.echo(f"{level.name}: {[name for name in result[result_level].keys()]}")
                click.echo()

            if self.level == level.name:
                break
    
    def print_error(self, error) -> None:
        if not self.summary:
            HEADER = """\n**ERROR**"""
            FORMAT = "{:<20} {:<40}"
            
            click.echo(HEADER)
            click.echo(FORMAT.format('package_name', 'error_reason')) 
            
            for package_name, error_reason in error.items():
                click.echo(FORMAT.format(package_name, error_reason)) 
            
            click.echo("-" * 80)

        else:
            click.echo(f"\nERROR: {[name for name in error.keys()]}")