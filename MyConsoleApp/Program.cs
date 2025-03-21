using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using OfficeOpenXml;

class Program
{
    static void Main(string[] args)
    {
        string pythonScriptPath = @"C:\Users\Анна\Desktop\control\jopSQLite.py";
        string dropTableScriptPath = @"C:\Users\Анна\Desktop\control\dropTable.py";
        string excelFilePath = @"C:\Users\Анна\Desktop\output.xlsx";

        string result = RunPythonScript(pythonScriptPath);
        if (result == null)
        {
            Console.WriteLine("Не удалось выполнить основной скрипт.");
            return;
        }

        if (WriteToExcel(result, excelFilePath))
        {
            Console.WriteLine("Данные успешно записаны в Excel файл.");
        }
        else
        {
            Console.WriteLine("Не удалось записать данные в Excel файл.");
        }

        string dropTableResult = RunPythonScript(dropTableScriptPath);
        if (dropTableResult == null)
        {
            Console.WriteLine("Не удалось выполнить скрипт для удаления таблицы.");
            return;
        }
    }

    static string RunPythonScript(string scriptPath)
    {
        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = $"\"{scriptPath}\"",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        try
        {
            using (Process process = Process.Start(startInfo))
            {
                if (process == null)
                {
                    Console.WriteLine("Не удалось запустить процесс.");
                    return null;
                }

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine("Ошибка при выполнении скрипта:");
                    Console.WriteLine(error);
                    return null;
                }

                return output;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Произошла ошибка при запуске скрипта: {ex.Message}");
            return null;
        }
    }

    static bool WriteToExcel(string data, string filePath)
    {
        try
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

            using (var package = new ExcelPackage())
            {
                var worksheet = package.Workbook.Worksheets.Add("Output");
                var lines = data.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries);

                for (int i = 0; i < lines.Length; i++)
                {
                    worksheet.Cells[i + 1, 1].Value = lines[i];
                }

                FileInfo fi = new FileInfo(filePath);
                package.SaveAs(fi);
            }

            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Ошибка при записи в Excel: {ex.Message}");
            return false;
        }
    }
}