<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\DB;

class BarcodeNutritionDetectionController extends Controller
{
    public function detectBarcodeNutrition(Request $request)
    {
        // Ganti URL sesuai kebutuhan
        $apiUrl = 'http://34.171.82.75/find_barcode';

        // Ambil nilai barcode dari permintaan
        $barcode = $request->input('barcode', '');

        // Kirim permintaan ke API eksternal
        $response = Http::get("$apiUrl?barcode=$barcode");

        // Periksa apakah permintaan berhasil
        if ($response->successful()) {
            // Parsing respon JSON
            $productNutritionData = $response->json();

            // Cek apakah ada nilai -01 pada respons
            if ($this->hasMissingData($productNutritionData)) {
                // Jika ada nilai -01, berikan respons khusus untuk mengisi data
                return response()->json(['message' => 'Data nutrisi produk belum lengkap, mohon lengkapi data.'], 200);
            }

            // Simpan data nutrisi produk ke dalam database lokal
            if ($this->saveProductNutritionDataLocally(auth()->id(), $productNutritionData)) {
                // Jika berhasil disimpan, berikan respons sukses
                return response()->json(['message' => 'Data nutrisi produk berhasil disimpan secara lokal.'], 200);
            } else {
                // Jika gagal disimpan, berikan respons gagal
                return response()->json(['error' => 'Failed to save product nutrition data locally.'], 500);
            }
        } else {
            // Jika permintaan gagal, kembalikan pesan kesalahan
            return response()->json(['error' => 'Failed to fetch product nutrition data.'], 500);
        }
    }

    private function hasMissingData($productNutritionData)
    {
        // Cek apakah ada nilai -01 pada respons nutrisi produk
        return in_array('-01', $productNutritionData);
    }

    public function saveProductNutritionLocally(Request $request)
    {
        // Ambil data nutrisi dari permintaan
        $data = $request->all();

        // Validasi data jika diperlukan
        // ...

        // Simpan data nutrisi produk ke dalam database lokal
        $saved = $this->saveProductNutritionDataLocally(auth()->id(), $data);

        // Berikan respons sesuai dengan hasil penyimpanan
        if ($saved) {
            return response()->json(['message' => 'Data nutrisi produk berhasil disimpan secara lokal.'], 200);
        } else {
            return response()->json(['error' => 'Gagal menyimpan data nutrisi produk secara lokal.'], 500);
        }
    }

    private function saveProductNutritionDataLocally($userId, $productNutritionData)
    {
        // Simpan data nutrisi produk ke dalam tabel 'nutrition_results' di localhost
        return DB::table('nutrition_results_local')->insert([
            'userid' => $userId,
            'calories' => $productNutritionData['calories'] ?? null,
            'carbs' => null, // Sesuaikan dengan struktur tabel Anda
            'fat' => $productNutritionData['fat'] ?? null,
            'protein' => null, // Sesuaikan dengan struktur tabel Anda
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }
}
