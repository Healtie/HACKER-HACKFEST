<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ImgUploadController;
use App\Http\Controllers\NutritionDetectionController;
use App\Http\Controllers\BarcodeNutritionDetectionController;
use App\Http\Controllers\WorkoutController;
/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('img-upload', [ImgUploadController::class, 'upload']);
Route::get('detect-nutrition', [NutritionDetectionController::class, 'detectNutrition']);
Route::get('get-daily-nutrition', [NutritionDetectionController::class, 'getDailyNutrition']);
Route::get('get-monthly-nutrition', [NutritionDetectionController::class, 'getMonthlyNutrition']);
Route::get('get-yearly-nutrition', [NutritionDetectionController::class, 'getYearlyNutrition']);
Route::get('detect-barcode-nutrition', [BarcodeNutritionDetectionController::class, 'detectBarcodeNutrition']);
Route::post('save-nutrition-locally', [BarcodeNutritionDetectionController::class, 'saveProductNutritionLocally']);

Route::get('workout/calories-today/{userId}', [WorkoutController::class, 'getCaloriesToday']);
Route::get('workout/calories-this-week/{userId}', [WorkoutController::class, 'getCaloriesThisWeek']);
Route::get('workout/recommended', [WorkoutController::class, 'getRecommendedWorkouts']);
