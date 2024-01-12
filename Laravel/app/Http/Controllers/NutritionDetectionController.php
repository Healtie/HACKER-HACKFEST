<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\DB;

class NutritionDetectionController extends Controller
{
    public function detectNutrition(Request $request)
    {
        // Ganti URL sesuai kebutuhan
        $apiUrl = 'http://34.171.82.75/classify_image';

        // Ganti 'custom.jpg' dengan nama file gambar yang ingin Anda kirimkan
        $imageUrl = 'custom.jpg';

        // Kirim permintaan ke API eksternal
        $response = Http::get("$apiUrl?uri=$imageUrl");

        // Periksa apakah permintaan berhasil
        if ($response->successful()) {
            // Parsing respon JSON
            $nutritionData = $response->json();

            // Simpan data nutrisi ke dalam database
            $this->saveNutritionData(auth()->id(), $nutritionData);

            // Mengembalikan respon dalam format JSON
            return response()->json($nutritionData, 200);
        } else {
            // Jika permintaan gagal, kembalikan pesan kesalahan
            return response()->json(['error' => 'Failed to fetch nutrition data.'], 500);
        }
    }

    private function saveNutritionData($userId, $nutritionData)
    {
        // Simpan data nutrisi ke dalam tabel 'nutrition_results'
        DB::table('nutrition_results')->insert([
            'userid' => $userId,
            'calories' => $nutritionData['calories'] ?? null,
            'carbs' => $nutritionData['carbs'] ?? null,
            'fat' => $nutritionData['fat'] ?? null,
            'protein' => $nutritionData['protein'] ?? null,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }

    public function getDailyNutrition()
    {
        $userId = auth()->id();

        $dailyNutrition = DB::table('nutrition_results')
            ->selectRaw('DATE(created_at) as date, SUM(calories) as total_calories, SUM(carbs) as total_carbs, SUM(fat) as total_fat, SUM(protein) as total_protein')
            ->where('userid', $userId)
            ->groupBy('date')
            ->get();

        return response()->json($dailyNutrition, 200);
    }

    public function getMonthlyNutrition()
    {
        $userId = auth()->id();

        $monthlyNutrition = DB::table('nutrition_results')
            ->selectRaw('YEAR(created_at) as year, MONTH(created_at) as month, SUM(calories) as total_calories, SUM(carbs) as total_carbs, SUM(fat) as total_fat, SUM(protein) as total_protein')
            ->where('userid', $userId)
            ->groupBy('year', 'month')
            ->get();

        return response()->json($monthlyNutrition, 200);
    }

    public function getYearlyNutrition()
    {
        $userId = auth()->id();

        $yearlyNutrition = DB::table('nutrition_results')
            ->selectRaw('YEAR(created_at) as year, SUM(calories) as total_calories, SUM(carbs) as total_carbs, SUM(fat) as total_fat, SUM(protein) as total_protein')
            ->where('userid', $userId)
            ->groupBy('year')
            ->get();

        return response()->json($yearlyNutrition, 200);
    }

    
}
